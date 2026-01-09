# base_input_tester_1_7.py
import win32api
import win32gui
import win32con
import random
import time
from ctypes import (
    windll,
    byref,
    c_ulong,
)
import threading
from contextlib import contextmanager
import logging
from datetime import datetime
import os
import psutil
import json

"""
BaseInputTester - Base class for isolated input testing utilities.

This module provides common functionality for creating isolated testing environments
for input devices like keyboards and mice. It handles window creation and management,
message processing, resource monitoring, and logging.

Version 1.8 Updates:
- Implemented missing check_and_monitor_resources method
- Removed duplicate code in testing loop
- Enhanced error handling in configuration loading
- Added support for console_logging_enabled configuration option
"""

# Make sure that GetWindowThreadProcessId(hwnd) is defined
if not hasattr(win32gui, "GetWindowThreadProcessId"):
    def GetWindowThreadProcessId(hwnd):
        """
        Replacement for win32gui.GetWindowThreadProcessId using ctypes.

        This function provides a fallback implementation if the method is not available
        in the win32gui module. It retrieves the thread and process IDs that created
        the specified window.

        Args:
            hwnd (int): Handle to the window.

        Returns:
            tuple: A tuple containing (thread_id, process_id).
        """
        pid = c_ulong()
        tid = windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        return tid, pid.value

    # Add the function to win32gui module
    win32gui.GetWindowThreadProcessId = GetWindowThreadProcessId


class BaseInputTester:
    """
    Base class for input testing in isolated environments.

    This class provides common functionality for creating hidden/transparent windows,
    message processing, resource monitoring, and logging. It is designed to be subclassed
    by specific input device testers like keyboard or mouse testers.

    Attributes:
        running (bool): Flag indicating whether the test is currently running.
        test_window (int): Handle to the test window.
        event_count (int): Counter for the number of events simulated.
        config (dict): Configuration parameters loaded from config file.
        cleanup_interval (int): Number of seconds between window cleanups.
        last_cleanup_time (float): Timestamp of the last window cleanup.
        message_process_interval (int): Number of seconds between message processing.
        last_message_process_time (float): Timestamp of the last message processing.
        resource_monitor_interval (int): Number of seconds between resource monitoring.
        last_resource_monitor_time (float): Timestamp of the last resource monitoring.
        process (psutil.Process): Current process for resource monitoring.
    """

    def __init__(self, config_file=None):
        """
        Initialize the BaseInputTester with default or config file parameters.

        Args:
            config_file (str, optional): Path to configuration file. Defaults to None.
        """
        self.running = False
        self.test_window = None
        self.event_count = 0

        # Load configuration if file provided, otherwise use defaults
        self.config = self.load_config(config_file)

        # Window management timers
        self.cleanup_interval = self.config.get("cleanup_interval", 600)  # 10 minutes
        self.last_cleanup_time = time.time()

        # Message processing timers
        self.message_process_interval = self.config.get("message_process_interval", 5)
        self.last_message_process_time = time.time()

        # Resource monitoring timers
        self.resource_monitor_interval = self.config.get("resource_monitor_interval", 30)
        self.last_resource_monitor_time = time.time()

        # Process for resource monitoring
        self.process = psutil.Process(os.getpid())

        # Set up logging
        self.setup_logging()

    def load_config(self, config_file):
        """
        Load configuration from a JSON file.

        Reads parameters from a JSON configuration file if provided,
        otherwise returns default configuration values. Supports both
        "config" and "config.json" file patterns.

        Args:
            config_file (str): Path to configuration file.

        Returns:
            dict: Configuration parameters.
        """
        default_config = {
            "cleanup_interval": 600,  # 10 minutes
            "message_process_interval": 5,  # 5 seconds
            "resource_monitor_interval": 30,  # 30 seconds
            "log_level": "INFO",
            "console_logging_enabled": True,  # Default to showing console logs
        }

        if config_file:
            try:
                # Handle JSON with comments
                with open(config_file, 'r') as f:
                    content = ""
                    for line in f:
                        # Remove comments (// style)
                        line_no_comment = line.split('//')[0] if '//' in line else line
                        # Also handle JSON /* */ style comments
                        if '/*' in line_no_comment and '*/' in line_no_comment:
                            line_no_comment = line_no_comment.split('/*')[0] + line_no_comment.split('*/')[1]
                        elif '/*' in line_no_comment:
                            line_no_comment = line_no_comment.split('/*')[0]
                        elif '*/' in line_no_comment:
                            line_no_comment = line_no_comment.split('*/')[1]

                        if line_no_comment.strip():
                            content += line_no_comment

                try:
                    config = json.loads(content)
                    # Merge with defaults (to ensure all required keys exist)
                    merged_config = default_config.copy()
                    merged_config.update(config)
                    self._print_message(f"Successfully loaded config from: {config_file}")
                    return merged_config
                except json.JSONDecodeError as e:
                    self._print_message(f"Error parsing JSON from {config_file}: {e}")
                    return default_config
            except Exception as e:
                self._print_message(f"Error loading config file {config_file}: {e}")
                return default_config

        self._print_message("No config file specified. Using default values.")
        return default_config

    def _print_message(self, message):
        """
        Print a message to console before logging is set up.

        Args:
            message (str): The message to print.
        """
        print(f"[{self.__class__.__name__}] {message}")

    def setup_logging(self):
        """
        Set up the logging system for the input tester.

        Creates a timestamped log file in a 'logs' directory relative to the script location.
        The log records all test activities with timestamps and severity levels.
        Respects the console_logging_enabled configuration option.
        """
        # Get script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logs_dir = os.path.join(script_dir, "logs")

        # Create logs directory relative to script location
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create log filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(logs_dir, f"{self.__class__.__name__.lower()}_{timestamp}.log")

        # Configure logging
        log_level = getattr(logging, self.config.get("log_level", "INFO"))

        # Setup handlers based on configuration
        handlers = [logging.FileHandler(log_filename)]

        # Add console handler only if enabled in config
        if self.config.get("console_logging_enabled", True):
            handlers.append(logging.StreamHandler())

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=handlers
        )

        self.logger.info(f"Starting new {self.__class__.__name__} session (v1.8)")
        self.logger.info(f"Log file: {os.path.abspath(log_filename)}")
        self.logger.info(f"Configuration: {self.config}")

    def window_proc(self, hwnd, msg, wparam, lparam):
        """
        Window procedure to handle window messages.

        This function is called by Windows whenever a message is sent to the
        test window. It passes the message to the default window
        procedure for standard handling.

        Args:
            hwnd (int): Handle to the window.
            msg (int): The message identifier.
            wparam (int): Additional message-specific information.
            lparam (int): Additional message-specific information.

        Returns:
            int: The result of the message processing.
        """
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

    def create_test_window(self):
        """
        Create a test window for input event simulation.

        This is an abstract method that should be implemented by subclasses
        to create an appropriate window for the specific input device testing.
        """
        raise NotImplementedError("Subclasses must implement create_test_window()")

    def process_messages(self):
        """
        Process any pending window messages to prevent queue buildup.

        This function retrieves and dispatches all queued messages for the window,
        helping to prevent the Windows message queue from becoming too full and
        causing resource exhaustion.
        """
        if not self.test_window:
            return

        # Create a MSG structure
        msg = win32gui.MSG()

        # Use PeekMessage with the correct number of arguments
        while win32gui.PeekMessage(msg, self.test_window, 0, 0, win32con.PM_REMOVE):
            win32gui.TranslateMessage(msg)
            win32gui.DispatchMessage(msg)

    def cleanup_window(self):
        """
        Perform periodic cleanup by destroying and recreating the window.

        This helps prevent resource leaks and message queue buildup by completely
        refreshing the window and its associated resources.
        """
        self.logger.info("Performing window cleanup...")
        if self.test_window:
            win32gui.DestroyWindow(self.test_window)
            self.test_window = None

        # Short delay to ensure cleanup completes
        time.sleep(0.5)

        # Create a new window
        self.create_test_window()
        self.last_cleanup_time = time.time()
        self.logger.info("Window cleanup completed")

    def monitor_resources(self):
        """
        Monitor and log system resource usage.

        Collects and logs memory and CPU usage of the current process,
        which helps track resource consumption during extended tests.
        """
        try:
            # Get CPU percent (interval=None means "since last call")
            cpu_percent = self.process.cpu_percent(interval=0.1)

            # Get memory info
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB

            # Log resource usage
            self.logger.info(f"Resource usage - CPU: {cpu_percent:.1f}%, Memory: {memory_mb:.2f} MB")

            # Update last monitor time
            self.last_resource_monitor_time = time.time()
        except Exception as e:
            self.logger.error(f"Error monitoring resources: {e}")

    def check_and_process_messages(self):
        """
        Check if it's time to process messages and do so if needed.
        """
        current_time = time.time()
        if current_time - self.last_message_process_time >= self.message_process_interval:
            self.process_messages()
            self.last_message_process_time = current_time

    def check_and_cleanup_window(self):
        """
        Check if it's time to perform window cleanup and do so if needed.
        """
        current_time = time.time()
        if current_time - self.last_cleanup_time >= self.cleanup_interval:
            self.cleanup_window()

    def check_and_monitor_resources(self):
        """
        Check if it's time to monitor resources and do so if needed.

        This method checks whether enough time has passed since resources were
        last monitored. If sufficient time has passed (based on the configured
        resource_monitor_interval), it calls the monitor_resources method to
        check CPU and memory usage.
        """
        current_time = time.time()
        if current_time - self.last_resource_monitor_time >= self.resource_monitor_interval:
            self.monitor_resources()

    @property
    def logger(self):
        """
        Get the logger instance.

        This property provides access to the logging module's logger,
        allowing for consistent logging across the class.

        Returns:
            logging.Logger: The logger instance.
        """
        return logging.getLogger()

    @contextmanager
    def test_window_context(self):
        """
        Context manager for the test window.

        Creates the test window when entering the context and ensures
        it is properly destroyed when exiting, even if an exception occurs.
        This guarantees proper resource cleanup.

        Yields:
            None
        """
        try:
            self.create_test_window()
            yield
        finally:
            if self.test_window:
                win32gui.DestroyWindow(self.test_window)
                self.test_window = None
                self.logger.info("Window destroyed during context exit")

    def simulate_input_event(self):
        """
        Simulate a random input event.

        This is an abstract method that should be implemented by subclasses
        to simulate appropriate events for the specific input device.
        """
        raise NotImplementedError("Subclasses must implement simulate_input_event()")

    def start_testing(self, min_interval=None, max_interval=None):
        """
        Start the input testing process.

        Creates a dedicated thread for simulating input at random intervals.
        The main thread monitors for the Escape key to terminate testing.
        All activity is logged to the log file.

        Args:
            min_interval (float, optional): Minimum time between events in seconds.
                If None, uses the value from config. Defaults to None.
            max_interval (float, optional): Maximum time between events in seconds.
                If None, uses the value from config. Defaults to None.
        """
        # Use provided intervals or fall back to config values
        min_interval = min_interval or self.config.get("event_interval_min", 1.0)
        max_interval = max_interval or self.config.get("event_interval_max", 5.0)

        self.logger.info(f"Starting {self.__class__.__name__} with intervals: min={min_interval}s, max={max_interval}s")
        self.logger.info("Press 'Esc' to stop testing")

        self.running = True
        self.event_count = 0
        self.last_cleanup_time = time.time()
        self.last_message_process_time = time.time()
        self.last_resource_monitor_time = time.time()

        # Initial resource monitoring
        self.monitor_resources()

        def testing_loop():
            """
            Inner function that runs the continuous input simulation.

            Creates the test window and simulates input events at random intervals
            until the testing is stopped. Includes periodic message processing,
            window cleanup, and resource monitoring to prevent resource exhaustion.
            """
            with self.test_window_context():
                while self.running:
                    try:
                        # Simulate input event
                        self.simulate_input_event()

                        # Process messages after each event
                        self.process_messages()

                        # Check for window cleanup and resource monitoring
                        self.check_and_cleanup_window()
                        self.check_and_monitor_resources()

                        # Wait until next event
                        interval = random.uniform(min_interval, max_interval)
                        self.logger.info(f"Waiting {interval:.2f} seconds until next event...")

                        # Break the waiting period into chunks to allow for more responsive termination
                        wait_end_time = time.time() + interval
                        while time.time() < wait_end_time and self.running:
                            time.sleep(0.1)
                            # Check if we should process messages during this wait
                            self.check_and_process_messages()

                    except Exception as e:
                        self.logger.error(f"Error in testing loop: {e}")
                        # Allow recovery from transient errors
                        time.sleep(5)
                        # Recreate window if needed
                        if not self.test_window:
                            self.create_test_window()

        # Create and start the testing thread
        test_thread = threading.Thread(target=testing_loop)
        test_thread.daemon = True
        test_thread.start()

        try:
            while self.running:
                if win32api.GetAsyncKeyState(win32con.VK_ESCAPE) & 0x8000:
                    break
                time.sleep(0.1)
        finally:
            self.running = False
            test_thread.join(timeout=1.0)

        # Final resource monitoring
        self.monitor_resources()

        self.logger.info(f"Testing completed. Total events simulated: {self.event_count}")


if __name__ == "__main__":
    print("BaseInputTester is a base class and should not be run directly.")
    print("Please use a specialized class like SafeKeyboardTester or SafeMouseTester instead.")
