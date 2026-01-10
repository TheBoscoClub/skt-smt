# smt-1.7.py
import win32api
import win32gui
import win32con
import random
import time
import os
import math
from ctypes import (
    windll,
    Structure,
    c_long,
    POINTER,
)
from base_input_tester_1_7 import BaseInputTester

"""
SafeMouseTester v1.7 - An advanced utility for testing mouse input in an isolated environment.

This script creates a hidden window to simulate mouse events without affecting other
applications. It generates advanced mouse movement patterns, clicks, and scrolls with
configurable timing and behavior, logging all activities for analysis.

It inherits common functionality from BaseInputTester and adds mouse-specific features.

New in v1.7:
- Updated to work with BaseInputTester v1.7
- Fixed compatibility with configuration file naming (.config or .config.json)
- Improved error handling and logging
- Implemented console_logging_enabled configuration option
- Standardized version numbering throughout code
"""

# Windows message constants for mouse events
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MOUSEWHEEL = 0x020A
WM_LBUTTONDBLCLK = 0x0203


class MSLLHOOKSTRUCT(Structure):
    """
    Structure that contains information about a low-level mouse input event.

    This structure mirrors the Windows MSLLHOOKSTRUCT used by the mouse hook procedure
    to pass mouse input to an application.

    Attributes:
        pt_x (c_long): x-coordinate of the mouse position.
        pt_y (c_long): y-coordinate of the mouse position.
        mouseData (c_long): Additional data for the mouse event (like wheel delta).
        flags (c_long): Flags that indicate various aspects of the mouse event.
        time (c_long): Timestamp for the event, in milliseconds.
        dwExtraInfo (POINTER(c_long)): Additional information associated with the message.
    """
    _fields_ = [
        ("pt_x", c_long),
        ("pt_y", c_long),
        ("mouseData", c_long),
        ("flags", c_long),
        ("time", c_long),
        ("dwExtraInfo", POINTER(c_long)),
    ]


class SafeMouseTester(BaseInputTester):
    """
    An advanced class for testing mouse input in an isolated environment.

    This class inherits from BaseInputTester and adds mouse-specific functionality.
    It creates a hidden window that simulates mouse events without interfering
    with other applications. It generates complex mouse movements, clicks, and scrolls
    to test mouse functionality.

    Attributes:
        hidden_window (int): Handle to the hidden window.
        screen_width (int): Width of the primary screen in pixels.
        screen_height (int): Height of the primary screen in pixels.
        current_x (int): Current x-coordinate of the simulated mouse position.
        current_y (int): Current y-coordinate of the simulated mouse position.
        movement_patterns (list): List of available movement patterns.
        movement_pattern_weights (list): Weights for selecting different movement patterns.
        current_movement_pattern (str): The currently active movement pattern.
    """

    def __init__(self, config_file="smt.config"):
        """
        Initialize the SafeMouseTester with parameters from config file.

        Args:
            config_file (str, optional): Path to configuration file. Defaults to "smt.config".
        """
        super().__init__(config_file)

        # Initialize window handles to None
        self.hidden_window = None
        self.test_window = None

        # Get screen dimensions
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)

        # Set default starting position to center of screen
        self.current_x = self.screen_width // 2
        self.current_y = self.screen_height // 2

        # Movement patterns
        self.movement_patterns = self.config.get("movement_patterns", ["random"])
        self.movement_pattern_weights = self.config.get("movement_pattern_weights", [1.0])
        # Ensure weights list is the same length as patterns list
        if len(self.movement_pattern_weights) < len(self.movement_patterns):
            self.movement_pattern_weights.extend([1.0] * (len(self.movement_patterns) - len(self.movement_pattern_weights)))
        self.current_movement_pattern = None

        # Cache frequently used config values
        self.movement_min_distance = self.config.get("movement_min_distance", 10)
        self.movement_max_distance = self.config.get("movement_max_distance", 100)
        self.click_probability = self.config.get("click_probability", 0.2)
        self.scroll_probability = self.config.get("scroll_probability", 0.1)
        self.double_click_probability = self.config.get("double_click_probability", 0.05)

        # Button types and weights
        self.button_types = self.config.get("button_types", ["left", "right", "middle"])
        self.button_weights = self.config.get("button_weights", [0.7, 0.2, 0.1])

        # Targeted movement targets
        self.targeted_targets = self.config.get("targeted_targets", [{"x_ratio": 0.5, "y_ratio": 0.5, "weight": 5}])

        # Circular movement parameters
        self.circular_min_radius = self.config.get("circular_min_radius", 20)
        self.circular_max_radius = self.config.get("circular_max_radius", 150)
        self.circular_min_steps = self.config.get("circular_min_steps", 8)
        self.circular_max_steps = self.config.get("circular_max_steps", 24)

        # Linear movement parameters
        self.linear_min_steps = self.config.get("linear_min_steps", 5)
        self.linear_max_steps = self.config.get("linear_max_steps", 20)

    def create_test_window(self):
        """
        Create a hidden window for mouse event simulation.

        This window is invisible to the user but can receive and process mouse events.
        It is used as a target for the simulated mouse events without affecting
        other applications.
        """
        windll.user32.SetProcessDPIAware()

        # Register window class
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "IsolatedMouseTester"
        wc.hInstance = win32api.GetModuleHandle(None)

        try:
            win32gui.RegisterClass(wc)
        except Exception:
            # Class might already be registered, which is fine
            pass

        # Create hidden window (1x1 pixel)
        self.hidden_window = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
            wc.lpszClassName,
            "Isolated Mouse Test",
            win32con.WS_POPUP,  # Hidden window
            0,
            0,
            1,
            1,  # 1x1 pixel size
            0,
            0,
            wc.hInstance,
            None,
        )

        # Set layered window attributes (just in case we make it visible for debugging)
        win32gui.SetLayeredWindowAttributes(
            self.hidden_window, 0, 1, win32con.LWA_ALPHA
        )

        # Store window handle in both attributes for compatibility
        self.test_window = self.hidden_window

        self.logger.info(f"Created new hidden window with handle: {self.hidden_window}")

    def simulate_mouse_move(self, to_x, to_y):
        """
        Simulate a mouse movement to a specific position.

        Sends a mouse move message to the hidden window. The coordinates
        are packed into the lparam parameter according to Windows API conventions.

        Args:
            to_x (int): The x-coordinate to move to.
            to_y (int): The y-coordinate to move to.

        Returns:
            bool: True if the movement was simulated, False otherwise.
        """
        if self.hidden_window:
            try:
                # Ensure coordinates are within screen bounds
                to_x = max(0, min(self.screen_width - 1, to_x))
                to_y = max(0, min(self.screen_height - 1, to_y))

                # Pack coordinates into lparam (low-order word has x, high-order word has y)
                lparam = to_y << 16 | to_x

                # Send mouse move message
                win32gui.PostMessage(self.hidden_window, WM_MOUSEMOVE, 0, lparam)

                # Update current position
                self.current_x = to_x
                self.current_y = to_y

                self.event_count += 1
                return True
            except Exception as e:
                self.logger.error(f"Error simulating mouse move: {e}")
                return False
        return False

    def simulate_mouse_click(self, button_type="left", double_click=False):
        """
        Simulate a mouse click at the current position.

        Sends mouse button down and up messages to the hidden window to simulate a click.
        Can also simulate double-click by sending the sequence twice with appropriate timing.

        Args:
            button_type (str, optional): The type of mouse button to simulate.
                Can be "left", "right", or "middle". Defaults to "left".
            double_click (bool, optional): Whether to simulate a double-click. Defaults to False.

        Returns:
            bool: True if the click was simulated, False otherwise.
        """
        if self.hidden_window:
            try:
                # Pack coordinates into lparam
                lparam = self.current_y << 16 | self.current_x

                # Determine message types based on button
                if button_type == "left":
                    down_msg = WM_LBUTTONDOWN
                    up_msg = WM_LBUTTONUP
                    dblclk_msg = WM_LBUTTONDBLCLK
                elif button_type == "right":
                    down_msg = WM_RBUTTONDOWN
                    up_msg = WM_RBUTTONUP
                    dblclk_msg = None  # No standard right double-click message
                elif button_type == "middle":
                    down_msg = WM_MBUTTONDOWN
                    up_msg = WM_MBUTTONUP
                    dblclk_msg = None  # No standard middle double-click message
                else:
                    self.logger.warning(f"Invalid button type: {button_type}")
                    return False

                if double_click and button_type == "left":
                    # Send double-click message directly
                    win32gui.PostMessage(self.hidden_window, dblclk_msg, 0, lparam)

                    # Brief delay
                    time.sleep(0.05)

                    # Send button up to complete the double-click
                    win32gui.PostMessage(self.hidden_window, up_msg, 0, lparam)
                else:
                    # Send button down
                    win32gui.PostMessage(self.hidden_window, down_msg, 0, lparam)

                    # Brief delay between down and up
                    time.sleep(0.08)

                    # Send button up
                    win32gui.PostMessage(self.hidden_window, up_msg, 0, lparam)

                    # For double click, repeat the sequence with appropriate timing
                    if double_click:
                        time.sleep(0.05)  # Brief delay between clicks

                        # Send second click
                        win32gui.PostMessage(self.hidden_window, down_msg, 0, lparam)
                        time.sleep(0.08)
                        win32gui.PostMessage(self.hidden_window, up_msg, 0, lparam)

                self.event_count += 1
                return True
            except Exception as e:
                self.logger.error(f"Error simulating mouse click: {e}")
                return False
        return False

    def simulate_mouse_scroll(self, delta=120):
        """
        Simulate a mouse wheel scroll at the current position.

        Sends a mouse wheel message to the hidden window. The delta parameter
        determines the direction and amount of scrolling.

        Args:
            delta (int, optional): The scroll amount. Positive for scroll up,
                negative for scroll down. Defaults to 120 (scroll up).

        Returns:
            bool: True if the scroll was simulated, False otherwise.
        """
        if self.hidden_window:
            try:
                # Pack coordinates into lparam
                lparam = self.current_y << 16 | self.current_x

                # Set mouseData to the scroll delta
                mouseData = delta << 16

                # Send mousewheel message
                win32gui.PostMessage(self.hidden_window, WM_MOUSEWHEEL, mouseData, lparam)

                self.event_count += 1
                return True
            except Exception as e:
                self.logger.error(f"Error simulating mouse scroll: {e}")
                return False
        return False

    def simulate_random_movement(self):
        """
        Simulate a random mouse movement.

        Moves the mouse in a random direction by a random distance,
        ensuring the movement is at least the minimum distance and
        stays within screen boundaries.

        Returns:
            bool: True if the movement was simulated, False otherwise.
        """
        # Calculate random movement within bounds
        delta_x = random.randint(-self.movement_max_distance, self.movement_max_distance)
        delta_y = random.randint(-self.movement_max_distance, self.movement_max_distance)

        # Ensure movement is at least minimum distance
        distance = math.sqrt(delta_x**2 + delta_y**2)
        if distance < self.movement_min_distance:
            # Scale up to minimum distance
            scale_factor = self.movement_min_distance / distance
            delta_x = int(delta_x * scale_factor)
            delta_y = int(delta_y * scale_factor)

        # Calculate new position
        new_x = max(0, min(self.screen_width - 1, self.current_x + delta_x))
        new_y = max(0, min(self.screen_height - 1, self.current_y + delta_y))

        # Simulate the movement
        if self.simulate_mouse_move(new_x, new_y):
            self.logger.info(f"Event {self.event_count}: Mouse moved randomly from "
                           f"({self.current_x - delta_x}, {self.current_y - delta_y}) "
                           f"to ({new_x}, {new_y})")
            return True
        return False

    def simulate_linear_movement(self):
        """
        Simulate a linear mouse movement.

        Moves the mouse in a straight line from the current position to a
        random end position, with intermediate steps along the line to
        simulate realistic cursor movement.

        Returns:
            bool: True if the movement was simulated successfully, False otherwise.
        """
        # Determine random end point
        delta_x = random.randint(-self.movement_max_distance, self.movement_max_distance)
        delta_y = random.randint(-self.movement_max_distance, self.movement_max_distance)

        # Ensure movement is at least minimum distance
        distance = math.sqrt(delta_x**2 + delta_y**2)
        if distance < self.movement_min_distance:
            # Scale up to minimum distance
            scale_factor = self.movement_min_distance / distance
            delta_x = int(delta_x * scale_factor)
            delta_y = int(delta_y * scale_factor)

        # Calculate end position
        end_x = max(0, min(self.screen_width - 1, self.current_x + delta_x))
        end_y = max(0, min(self.screen_height - 1, self.current_y + delta_y))

        # Determine number of steps for this linear movement
        steps = random.randint(self.linear_min_steps, self.linear_max_steps)

        # Store starting position for logging
        start_x, start_y = self.current_x, self.current_y

        # Move in steps
        success = True
        for step in range(1, steps + 1):
            # Calculate position at this step
            step_x = int(start_x + (end_x - start_x) * step / steps)
            step_y = int(start_y + (end_y - start_y) * step / steps)

            # Simulate the movement
            if not self.simulate_mouse_move(step_x, step_y):
                success = False
                break

            # Small delay between steps
            time.sleep(0.01)

            # Process messages periodically
            self.check_and_process_messages()

        if success:
            self.logger.info(f"Event {self.event_count}: Mouse moved linearly from "
                           f"({start_x}, {start_y}) to ({end_x}, {end_y}) in {steps} steps")
            return True
        return False

    def simulate_circular_movement(self):
        """
        Simulate a circular mouse movement.

        Moves the mouse in a circular pattern around the current position,
        creating a realistic circular motion with configurable radius and steps.

        Returns:
            bool: True if the movement was simulated successfully, False otherwise.
        """
        # Determine circle parameters
        radius = random.randint(self.circular_min_radius, self.circular_max_radius)
        steps = random.randint(self.circular_min_steps, self.circular_max_steps)

        # Ensure circle stays within screen bounds
        center_x = max(radius, min(self.screen_width - radius, self.current_x))
        center_y = max(radius, min(self.screen_height - radius, self.current_y))

        # Move in a circle
        success = True
        for step in range(steps):
            # Calculate position on circle
            angle = 2 * math.pi * step / steps
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))

            # Ensure within screen bounds (should already be, but double-check)
            x = max(0, min(self.screen_width - 1, x))
            y = max(0, min(self.screen_height - 1, y))

            # Simulate the movement
            if not self.simulate_mouse_move(x, y):
                success = False
                break

            # Small delay between steps
            time.sleep(0.02)

            # Process messages periodically
            self.check_and_process_messages()

        if success:
            self.logger.info(f"Event {self.event_count}: Mouse moved in circular pattern "
                           f"around ({center_x}, {center_y}) with radius {radius}")
            return True
        return False

    def simulate_targeted_movement(self):
        """
        Simulate a mouse movement targeted at a specific location.

        Selects a target position from a predefined list of weighted targets,
        then moves the mouse to that target with a realistic motion pattern.
        Useful for simulating clicks on UI elements.

        Returns:
            bool: True if the movement was simulated successfully, False otherwise.
        """
        if not self.targeted_targets:
            return self.simulate_random_movement()

        # Select a target based on weights
        targets = []
        weights = []
        for target in self.targeted_targets:
            targets.append((
                int(target["x_ratio"] * self.screen_width),
                int(target["y_ratio"] * self.screen_height)
            ))
            weights.append(target.get("weight", 1))

        target_x, target_y = random.choices(targets, weights=weights, k=1)[0]

        # Calculate distance to target
        distance = math.sqrt((target_x - self.current_x)**2 + (target_y - self.current_y)**2)

        # Determine number of steps based on distance
        steps = max(5, min(20, int(distance / 10)))

        # Store starting position for logging
        start_x, start_y = self.current_x, self.current_y

        # Add slight curve to movement for realism
        curve_offset = int(distance * 0.1)  # 10% of distance
        midpoint_x = (start_x + target_x) / 2 + random.randint(-curve_offset, curve_offset)
        midpoint_y = (start_y + target_y) / 2 + random.randint(-curve_offset, curve_offset)

        # Move in steps with a slight curve
        success = True
        for step in range(1, steps + 1):
            # Calculate t parameter (0 to 1)
            t = step / steps

            # Quadratic Bezier curve formula
            x = int((1-t)**2 * start_x + 2*(1-t)*t * midpoint_x + t**2 * target_x)
            y = int((1-t)**2 * start_y + 2*(1-t)*t * midpoint_y + t**2 * target_y)

            # Ensure within screen bounds
            x = max(0, min(self.screen_width - 1, x))
            y = max(0, min(self.screen_height - 1, y))

            # Simulate the movement
            if not self.simulate_mouse_move(x, y):
                success = False
                break

            # Varying delay to simulate human acceleration/deceleration
            delay = 0.02
            if step < steps * 0.2 or step > steps * 0.8:
                delay = 0.03  # Slower at start and end
            time.sleep(delay)

            # Process messages periodically
            self.check_and_process_messages()

        if success:
            self.logger.info(f"Event {self.event_count}: Mouse moved to target "
                           f"from ({start_x}, {start_y}) to ({target_x}, {target_y})")
            return True
        return False

    def simulate_movement_pattern(self):
        """
        Select and simulate a mouse movement pattern based on weighted probabilities.

        Chooses a movement pattern from the configured list based on their weights,
        then simulates that pattern. This creates more realistic mouse behavior
        with varied patterns of movement.

        Returns:
            bool: True if the pattern was simulated successfully, False otherwise.
        """
        # Select a movement pattern
        self.current_movement_pattern = random.choices(
            self.movement_patterns,
            weights=self.movement_pattern_weights[:len(self.movement_patterns)],
            k=1
        )[0]

        # Execute the selected pattern
        if self.current_movement_pattern == "random":
            return self.simulate_random_movement()
        elif self.current_movement_pattern == "linear":
            return self.simulate_linear_movement()
        elif self.current_movement_pattern == "circular":
            return self.simulate_circular_movement()
        elif self.current_movement_pattern == "targeted":
            return self.simulate_targeted_movement()
        else:
            # Fall back to random movement if pattern not recognized
            self.logger.warning(f"Unknown movement pattern: {self.current_movement_pattern}. Falling back to random.")
            return self.simulate_random_movement()

    def simulate_input_event(self):
        """
        Simulate a mouse input event.

        Generates a random mouse event - either a movement pattern, a click, or a scroll,
        based on configured probabilities. This method is called by the base class's
        testing loop.

        Returns:
            bool: True if the event was simulated successfully, False otherwise.
        """
        # Decide what type of event to generate
        random_value = random.random()

        # Move the mouse (highest probability)
        if random_value >= (self.click_probability + self.scroll_probability):
            return self.simulate_movement_pattern()

        # Generate a mouse click
        elif random_value < self.click_probability:
            # Choose random button type based on weights
            button_type = random.choices(
                self.button_types,
                weights=self.button_weights[:len(self.button_types)],
                k=1
            )[0]

            # Decide if this is a double-click
            double_click = random.random() < self.double_click_probability and button_type == "left"

            # Simulate the click
            if self.simulate_mouse_click(button_type, double_click):
                click_type = "double-click" if double_click else "click"
                self.logger.info(f"Event {self.event_count}: {button_type.capitalize()} {click_type} at "
                               f"({self.current_x}, {self.current_y})")
                return True

        # Generate a mouse scroll
        else:
            # Random scroll amount (positive for up, negative for down)
            scroll_direction = 1 if random.random() > 0.5 else -1
            scroll_amount = random.randint(1, 3) * 120 * scroll_direction

            # Simulate the scroll
            if self.simulate_mouse_scroll(scroll_amount):
                direction = "up" if scroll_amount > 0 else "down"
                self.logger.info(f"Event {self.event_count}: Mouse scrolled {direction} at "
                               f"({self.current_x}, {self.current_y})")
                return True

        return False

    def cleanup_window(self):
        """
        Perform periodic cleanup by destroying and recreating the window.

        This overrides the base class method to handle the hidden_window attribute.
        This helps prevent resource leaks and message queue buildup by completely
        refreshing the window and its associated resources.
        """
        self.logger.info("Performing window cleanup...")
        if self.hidden_window:
            win32gui.DestroyWindow(self.hidden_window)
            self.hidden_window = None
            self.test_window = None

        # Short delay to ensure cleanup completes
        time.sleep(0.5)

        # Create a new window
        self.create_test_window()
        self.last_cleanup_time = time.time()
        self.logger.info("Window cleanup completed")


if __name__ == "__main__":
    """
    Main entry point for the SafeMouseTester script.

    Creates an instance of the SafeMouseTester class and starts the testing process
    with parameters from the configuration file. Any exceptions are logged and re-raised.

    The script accepts optional command-line arguments for min and max intervals,
    which override the configuration file values if provided.
    """
    import sys
    import logging

    print("SafeMouseTester v1.7 - Test mouse input in an isolated environment")
    print("Use 'ESC' key to stop testing")

    # Parse command line arguments for min/max intervals (optional)
    min_interval = None
    max_interval = None

    if len(sys.argv) > 1:
        try:
            min_interval = float(sys.argv[1])
            if len(sys.argv) > 2:
                max_interval = float(sys.argv[2])
            print(f"Using custom intervals: min={min_interval}s, max={max_interval}s")
        except ValueError:
            print("Invalid interval argument. Using config file values.")

    # Find config file in the same directory as the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "smt.config")

    # Create tester instance
    try:
        tester = SafeMouseTester(config_path if os.path.exists(config_path) else None)
        tester.start_testing(min_interval, max_interval)
    except Exception as e:
        logging.error(f"\nAn error occurred: {e}")
        print(f"\nError: {e}")
        print("Check the log file for more details.")
        input("Press Enter to exit...")
        raise
