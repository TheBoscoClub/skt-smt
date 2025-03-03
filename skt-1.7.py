# skt-1.7.py
import win32api
import win32gui
import win32con
import random
import time
import string
import os
import math
from ctypes import (
    windll,
    Structure,
    c_long,
    POINTER,
)
from base_input_tester_1.7 import BaseInputTester

"""
SafeKeyboardTester v1.7 - An advanced utility for testing keyboard input in an isolated environment.

This script creates a transparent overlay window to capture and simulate keyboard events
without affecting other applications. It generates realistic typing patterns with configurable
timing, character variations, and occasional typos, logging all activities for analysis.

It inherits common functionality from BaseInputTester and adds keyboard-specific features.

New in v1.7:
- Updated to work with BaseInputTester v1.7
- Fixed compatibility with configuration file naming (.config or .config.json)
- Improved error handling and logging
- Implemented console_logging_enabled configuration option
- Standardized version numbering throughout code
- Added validation of keyboard configurations
"""

# Windows message constants for keyboard events
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_CHAR = 0x0102

# Initialize virtual key code mapping at module level for efficiency
VK_CODES = {char: win32api.VkKeyScan(char) & 0xFF for char in string.ascii_lowercase + string.ascii_uppercase + string.digits}

# Special keys mapping
SPECIAL_KEYS = {
    "space": win32con.VK_SPACE,
    "enter": win32con.VK_RETURN,
    "backspace": win32con.VK_BACK,
    "tab": win32con.VK_TAB,
    "shift": win32con.VK_SHIFT,
    "ctrl": win32con.VK_CONTROL,
    "alt": win32con.VK_MENU,
    "capslock": win32con.VK_CAPITAL,
    "escape": win32con.VK_ESCAPE,
}

class KBDLLHOOKSTRUCT(Structure):
    """
    Structure that contains information about a low-level keyboard input event.

    This structure mirrors the Windows KBDLLHOOKSTRUCT used by the keyboard hook procedure
    to pass keyboard input to an application.

    Attributes:
        vkCode (c_long): Virtual-key code of the key.
        scanCode (c_long): Hardware scan code for the key.
        flags (c_long): Flags that indicate various aspects of the keystroke.
        time (c_long): Timestamp for the event, in milliseconds.
        dwExtraInfo (POINTER(c_long)): Additional information associated with the message.
    """
    _fields_ = [
        ("vkCode", c_long),
        ("scanCode", c_long),
        ("flags", c_long),
        ("time", c_long),
        ("dwExtraInfo", POINTER(c_long)),
    ]


class SafeKeyboardTester(BaseInputTester):
    """
    An advanced class for testing keyboard input in an isolated environment.

    This class inherits from BaseInputTester and adds keyboard-specific functionality.
    It creates a transparent overlay window that captures keyboard events without
    interfering with other applications. It simulates typing with realistic patterns,
    including common words, typos, and corrections.

    Attributes:
        letters (list): List of lowercase letters that can be typed.
        special_keys (dict): Dictionary mapping special key names to virtual key codes.
        current_typing_pattern (str): The currently active typing pattern.
        typing_pattern_weights (list): Weights for selecting different typing patterns.
    """

    def __init__(self, config_file="skt.config"):
        """
        Initialize the SafeKeyboardTester with parameters from config file.

        Args:
            config_file (str, optional): Path to configuration file. Defaults to "skt.config".
        """
        super().__init__(config_file)

        # Initialize window handles to None
        self.transparent_window = None
        self.test_window = None

        # Define character sets
        self.letters = list(string.ascii_lowercase)
        self.special_keys = SPECIAL_KEYS

        # Typing patterns
        self.typing_patterns = self.config.get("typing_patterns", ["common_word", "random_word"])

        # Create equal weights if none provided or if length doesn't match
        if "typing_pattern_weights" not in self.config or len(self.config.get("typing_pattern_weights", [])) != len(self.typing_patterns):
            self.typing_pattern_weights = [1.0] * len(self.typing_patterns)
        else:
            self.typing_pattern_weights = self.config.get("typing_pattern_weights")

        self.current_typing_pattern = None

        # Common words list
        self.common_words = self.config.get("common_words", ["the", "and", "to"])
        if not self.common_words:
            self.logger.warning("No common words found in configuration. Using default set.")
            self.common_words = ["the", "and", "to", "of", "a", "in", "is", "it", "you", "that"]

        # Cache frequently used config values
        self.key_interval_min = self.config.get("key_interval_min", 0.1)
        self.key_interval_max = self.config.get("key_interval_max", 0.3)
        self.word_length_min = self.config.get("word_length_min", 3)
        self.word_length_max = self.config.get("word_length_max", 8)
        self.typo_probability = self.config.get("typo_probability", 0.05)
        self.correction_probability = self.config.get("correction_probability", 0.8)
        self.capitalization_probability = self.config.get("capitalization_probability", 0.2)
        self.common_words_probability = self.config.get("common_words_probability", 0.7)
        self.special_key_probability = self.config.get("special_key_probability", 0.05)
        self.space_after_word_probability = self.config.get("space_after_word_probability", 0.9)

        # Validate configuration values
        self._validate_config()

    def _validate_config(self):
        """
        Validate configuration values and adjust if needed.

        This checks that probability values are between 0 and 1,
        and that interval values make logical sense.
        """
        # Validate probability values (must be between 0 and 1)
        prob_values = [
            ("typo_probability", self.typo_probability),
            ("correction_probability", self.correction_probability),
            ("capitalization_probability", self.capitalization_probability),
            ("common_words_probability", self.common_words_probability),
            ("special_key_probability", self.special_key_probability),
            ("space_after_word_probability", self.space_after_word_probability)
        ]

        for name, value in prob_values:
            if not 0 <= value <= 1:
                self.logger.warning(f"Invalid probability value for {name}: {value}. Must be between 0 and 1. Setting to default.")
                setattr(self, name, self.config.get(name, 0.5))

        # Validate interval values
        if self.key_interval_min < 0 or self.key_interval_min > self.key_interval_max:
            self.logger.warning(f"Invalid key_interval_min value: {self.key_interval_min}. Setting to default.")
            self.key_interval_min = 0.1

        if self.key_interval_max <= 0:
            self.logger.warning(f"Invalid key_interval_max value: {self.key_interval_max}. Setting to default.")
            self.key_interval_max = 0.3

        # Validate word length values
        if self.word_length_min < 1 or self.word_length_min > self.word_length_max:
            self.logger.warning(f"Invalid word_length_min value: {self.word_length_min}. Setting to default.")
            self.word_length_min = 3

        if self.word_length_max < 1:
            self.logger.warning(f"Invalid word_length_max value: {self.word_length_max}. Setting to default.")
            self.word_length_max = 8

    def create_test_window(self):
        """
        Create a transparent overlay window that covers the entire screen.

        This window is invisible to the user but captures keyboard input events.
        It is set to be topmost, layered, and transparent to allow normal interaction
        with applications underneath.

        The window is DPI-aware to ensure proper scaling on high-resolution displays.
        """
        windll.user32.SetProcessDPIAware()

        # Register window class
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.window_proc
        wc.lpszClassName = "IsolatedKeyboardTester"
        wc.hInstance = win32api.GetModuleHandle(None)

        try:
            win32gui.RegisterClass(wc)
        except Exception:
            # Class might already be registered, which is fine
            pass

        # Create transparent window
        self.transparent_window = win32gui.CreateWindowEx(
            win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
            wc.lpszClassName,
            "Isolated Keyboard Test",
            win32con.WS_POPUP,  # Removed WS_VISIBLE flag
            0,
            0,
            1,
            1,  # 1x1 pixel since it's hidden
            0,
            0,
            wc.hInstance,
            None,
        )

        # Make window transparent
        win32gui.SetLayeredWindowAttributes(
            self.transparent_window, 0, 1, win32con.LWA_ALPHA
        )

        # Store window handle in both attributes for compatibility
        self.test_window = self.transparent_window

        self.logger.info(f"Created new transparent window with handle: {self.transparent_window}")

    def simulate_keypress(self, vk_code, char=None):
        """
        Simulate a keypress in the isolated window.

        Posts keyboard messages to the transparent overlay window to simulate
        a key being pressed and released. Optionally sends a character message
        for printable characters.

        Args:
            vk_code (int): Virtual key code of the key to simulate.
            char (str, optional): Character to send with the WM_CHAR message. Defaults to None.

        Returns:
            bool: True if the keypress was simulated, False otherwise.
        """
        if self.transparent_window:
            try:
                # Send key down
                win32gui.PostMessage(self.transparent_window, WM_KEYDOWN, vk_code, 0)

                # Send character if provided
                if char:
                    win32gui.PostMessage(self.transparent_window, WM_CHAR, ord(char), 0)

                # Slight delay between down and up events
                time.sleep(0.08)

                # Send key up
                win32gui.PostMessage(self.transparent_window, WM_KEYUP, vk_code, 0)

                self.event_count += 1
                return True

            except Exception as e:
                self.logger.error(f"Error simulating keypress: {e}")
                return False
        return False


    def get_adjacent_keys(self, char):
        """
        Get adjacent keys on a QWERTY keyboard for a given character.

        Used for realistic typos by simulating pressing a key close to the intended one.

        Args:
            char (str): The character to find adjacent keys for.

        Returns:
            list: List of characters adjacent to the input character.
        """
        keyboard_layout = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\''],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
        ]

        # Convert to lowercase for searching
        char = char.lower()

        # Find position of character in keyboard layout
        row_idx, col_idx = -1, -1
        for i, row in enumerate(keyboard_layout):
            if char in row:
                row_idx = i
                col_idx = row.index(char)
                break

        if row_idx == -1:
            return self.letters  # Character not found, return all letters

        # Get adjacent keys
        adjacent = []
        for i in range(max(0, row_idx - 1), min(len(keyboard_layout), row_idx + 2)):
            for j in range(max(0, col_idx - 1), min(len(keyboard_layout[i]), col_idx + 2)):
                if not (i == row_idx and j == col_idx):  # Skip the original character
                    adjacent.append(keyboard_layout[i][j])

        return adjacent if adjacent else self.letters

    def generate_typo(self, char):
        """
        Generate a realistic typo for a given character.

        Args:
            char (str): The intended character.

        Returns:
            str: A character representing a realistic typo.
        """
        adjacent_keys = self.get_adjacent_keys(char)
        if adjacent_keys:
            return random.choice(adjacent_keys)
        return random.choice(self.letters)

    def simulate_typing_pattern(self):
        """
        Select and simulate a typing pattern based on weighted probabilities.

        Chooses a typing pattern from the configured list based on their weights,
        then simulates that pattern. This creates more realistic typing behavior
        with varied patterns of input.

        Returns:
            bool: True if the pattern was simulated successfully, False otherwise.
        """
        # Select a typing pattern
        self.current_typing_pattern = random.choices(
            self.typing_patterns,
            weights=self.typing_pattern_weights,
            k=1
        )[0]

        # Execute the selected pattern
        if self.current_typing_pattern == "common_word":
            return self.simulate_common_word()
        elif self.current_typing_pattern == "random_word":
            return self.simulate_random_word()
        elif self.current_typing_pattern == "sentence":
            return self.simulate_sentence()
        elif self.current_typing_pattern == "code_snippet":
            return self.simulate_code_snippet()
        elif self.current_typing_pattern == "number_sequence":
            return self.simulate_number_sequence()
        else:
            # Fall back to random word if pattern not recognized
            self.logger.warning(f"Unknown typing pattern: {self.current_typing_pattern}. Falling back to random word.")
            return self.simulate_random_word()

    def simulate_common_word(self):
        """
        Simulate typing a common English word.

        Selects a word from the common words list and types it with
        realistic timing, potential typos, and corrections.

        Returns:
            bool: True if the word was typed successfully, False otherwise.
        """
        if not self.common_words:
            self.logger.warning("No common words available. Falling back to random word.")
            return self.simulate_random_word()

        word = random.choice(self.common_words)
        typed_chars = []

        # Apply capitalization sometimes
        if random.random() < self.capitalization_probability:
            word = word.capitalize()

        for i, char in enumerate(word):
            # Decide if we make a typo
            if random.random() < self.typo_probability:
                typo = self.generate_typo(char)
                vk_code = VK_CODES.get(typo, VK_CODES.get(typo.lower(), 0))

                if vk_code and self.simulate_keypress(vk_code, typo):
                    typed_chars.append(typo)
                    char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                    time.sleep(char_delay)

                    # Decide if we correct the typo
                    if random.random() < self.correction_probability:
                        # Press backspace
                        if self.simulate_keypress(win32con.VK_BACK):
                            typed_chars.pop()  # Remove the typo
                            char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                            time.sleep(char_delay)

                            # Type the correct character
                            vk_code = VK_CODES.get(char, VK_CODES.get(char.lower(), 0))
                            if vk_code and self.simulate_keypress(vk_code, char):
                                typed_chars.append(char)
            else:
                # Type the correct character
                vk_code = VK_CODES.get(char, VK_CODES.get(char.lower(), 0))

                if vk_code and self.simulate_keypress(vk_code, char):
                    typed_chars.append(char)
                    char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                    time.sleep(char_delay)

            # Process messages periodically during typing to prevent queue buildup
            self.check_and_process_messages()

        # Add space after word (with configured probability)
        if random.random() < self.space_after_word_probability:
            if self.simulate_keypress(win32con.VK_SPACE, " "):
                typed_chars.append(" ")

        self.logger.info(f"Burst {self.event_count}: Simulated common word '{''.join(typed_chars)}'")
        return True

    def simulate_random_word(self):
        """
        Simulate typing a random word.

        Generates a random sequence of characters with configurable length and
        simulates typing it with realistic timing, potential typos, and corrections.

        Returns:
            bool: True if the word was typed successfully, False otherwise.
        """
        word_length = random.randint(self.word_length_min, self.word_length_max)
        typed_chars = []

        for _ in range(word_length):
            char = random.choice(self.letters)

            # Decide if we make a typo
            if random.random() < self.typo_probability:
                typo = self.generate_typo(char)
                vk_code = VK_CODES.get(typo, 0)

                if vk_code and self.simulate_keypress(vk_code, typo):
                    typed_chars.append(typo)
                    char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                    time.sleep(char_delay)

                    # Decide if we correct the typo
                    if random.random() < self.correction_probability:
                        # Press backspace
                        if self.simulate_keypress(win32con.VK_BACK):
                            typed_chars.pop()  # Remove the typo
                            char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                            time.sleep(char_delay)

                            # Type the correct character
                            vk_code = VK_CODES.get(char, 0)
                            if vk_code and self.simulate_keypress(vk_code, char):
                                typed_chars.append(char)
            else:
                # Type the correct character
                vk_code = VK_CODES.get(char, 0)

                if vk_code and self.simulate_keypress(vk_code, char):
                    typed_chars.append(char)
                    char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                    time.sleep(char_delay)

            # Process messages periodically during typing to prevent queue buildup
            self.check_and_process_messages()

        # Add space after word (with configured probability)
        if random.random() < self.space_after_word_probability:
            if self.simulate_keypress(win32con.VK_SPACE, " "):
                typed_chars.append(" ")

        self.logger.info(f"Burst {self.event_count}: Simulated random word '{''.join(typed_chars)}'")
        return True

    def simulate_sentence(self):
        """
        Simulate typing a sentence composed of multiple words.

        Generates a sentence by combining common and random words, adding
        appropriate punctuation, and simulating realistic typing behavior.

        Returns:
            bool: True if the sentence was typed successfully, False otherwise.
        """
        sentence_length = random.randint(3, 8)  # Number of words in the sentence
        typed_chars = []

        # First word is capitalized
        if random.random() < self.common_words_probability and self.common_words:
            word = random.choice(self.common_words).capitalize()
        else:
            word = random.choice(self.letters).upper() + ''.join(random.choice(self.letters) for _ in range(random.randint(2, 7)))

        # Type the first word
        for char in word:
            vk_code = VK_CODES.get(char, VK_CODES.get(char.lower(), 0))
            if vk_code and self.simulate_keypress(vk_code, char):
                typed_chars.append(char)
                char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                time.sleep(char_delay)

        # Type space after first word
        if self.simulate_keypress(win32con.VK_SPACE, " "):
            typed_chars.append(" ")

        # Type the rest of the words
        for i in range(1, sentence_length):
            # Process messages periodically
            self.check_and_process_messages()

            # Select common or random word
            if random.random() < self.common_words_probability and self.common_words:
                word = random.choice(self.common_words)
            else:
                word = ''.join(random.choice(self.letters) for _ in range(random.randint(2, 7)))

            # Type the word
            for char in word:
                vk_code = VK_CODES.get(char, 0)
                if vk_code and self.simulate_keypress(vk_code, char):
                    typed_chars.append(char)
                    char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                    time.sleep(char_delay)

            # Add space after word unless it's the last word
            if i < sentence_length - 1:
                if self.simulate_keypress(win32con.VK_SPACE, " "):
                    typed_chars.append(" ")

        # End the sentence with punctuation
        punctuation = random.choice(['.', '!', '?'])
        vk_code = win32api.VkKeyScan(punctuation) & 0xFF
        if self.simulate_keypress(vk_code, punctuation):
            typed_chars.append(punctuation)

        self.logger.info(f"Burst {self.event_count}: Simulated sentence '{''.join(typed_chars)}'")
        return True

    def simulate_code_snippet(self):
        """
        Simulate typing a simple code snippet.

        Generates and types a fragment that resembles programming code,
        including symbols, indentation, and typical programming constructs.

        Returns:
            bool: True if the code snippet was typed successfully, False otherwise.
        """
        # Select a code pattern
        code_patterns = [
            "if(x>0){{return true;}}",
            "for(int i=0;i<10;i++){{}}",
            "function test(){{return null;}}",
            "const x = [];",
            "let result = a + b;",
            "class Test{{constructor(){{}}}}",
            "import os\nprint('hello')",
            "def main():\n    return 0",
            "while(true){{break;}}"
        ]

        code = random.choice(code_patterns)
        typed_chars = []

        for char in code:
            # Handle special characters
            if char == '\n':
                vk_code = win32con.VK_RETURN
                if self.simulate_keypress(vk_code):
                    typed_chars.append('\n')
            elif char == '\t' or (char == ' ' and typed_chars and typed_chars[-1] == '\n'):
                vk_code = win32con.VK_TAB
                if self.simulate_keypress(vk_code):
                    typed_chars.append('    ')  # Represent tab as 4 spaces
            else:
                vk_code = win32api.VkKeyScan(char) & 0xFF
                if vk_code != -1 and self.simulate_keypress(vk_code, char):
                    typed_chars.append(char)

            char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
            time.sleep(char_delay)

            # Process messages periodically
            self.check_and_process_messages()

        self.logger.info(f"Burst {self.event_count}: Simulated code snippet '{''.join(typed_chars)}'")
        return True

    def simulate_number_sequence(self):
        """
        Simulate typing a sequence of numbers.

        Generates and types a random sequence of digits, which might represent
        a phone number, ID, or other numeric data.

        Returns:
            bool: True if the number sequence was typed successfully, False otherwise.
        """
        # Determine length of number sequence
        length = random.randint(3, 10)
        typed_chars = []

        for _ in range(length):
            digit = str(random.randint(0, 9))
            vk_code = VK_CODES.get(digit, 0)

            if vk_code and self.simulate_keypress(vk_code, digit):
                typed_chars.append(digit)
                char_delay = random.uniform(self.key_interval_min, self.key_interval_max)
                time.sleep(char_delay)

            # Process messages periodically
            self.check_and_process_messages()

        self.logger.info(f"Burst {self.event_count}: Simulated number sequence '{''.join(typed_chars)}'")
        return True

    def simulate_special_key(self):
        """
        Simulate pressing a special key.

        Selects a random special key (Enter, Tab, Backspace, etc.) and
        simulates pressing it.

        Returns:
            bool: True if the key press was simulated successfully, False otherwise.
        """
        key_name = random.choice(list(self.special_keys.keys()))
        vk_code = self.special_keys[key_name]

        if self.simulate_keypress(vk_code):
            self.logger.info(f"Burst {self.event_count}: Simulated special key '{key_name}'")
            return True
        return False

    def simulate_input_event(self):
        """
        Simulate a keyboard input event.

        Either generates a typing pattern or a special key press based on
        configured probabilities. This method is called by the base class's
        testing loop.

        Returns:
            bool: True if the event was simulated successfully, False otherwise.
        """
        if random.random() < self.special_key_probability:
            # Simulate special key
            return self.simulate_special_key()
        else:
            # Simulate typing pattern
            return self.simulate_typing_pattern()

    def cleanup_window(self):
        """
        Perform periodic cleanup by destroying and recreating the window.

        This overrides the base class method to handle the transparent_window attribute.
        This helps prevent resource leaks and message queue buildup by completely
        refreshing the window and its associated resources.
        """
        self.logger.info("Performing window cleanup...")
        if self.transparent_window:
            win32gui.DestroyWindow(self.transparent_window)
            self.transparent_window = None
            self.test_window = None

        # Short delay to ensure cleanup completes
        time.sleep(0.5)

        # Create a new window
        self.create_test_window()
        self.last_cleanup_time = time.time()
        self.logger.info("Window cleanup completed")


if __name__ == "__main__":
    """
    Main entry point for the SafeKeyboardTester script.

    Creates an instance of the SafeKeyboardTester class and starts the testing process
    with parameters from the configuration file. Any exceptions are logged and re-raised.

    The script accepts optional command-line arguments for min and max intervals,
    which override the configuration file values if provided.
    """
    import sys
    import logging

    print(f"SafeKeyboardTester v1.7 - Test keyboard input in an isolated environment")
    print(f"Use 'ESC' key to stop testing")

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
    config_path = os.path.join(script_dir, "skt.config")

    # Create tester instance
    try:
        tester = SafeKeyboardTester(config_path if os.path.exists(config_path) else None)
        tester.start_testing(min_interval, max_interval)
    except Exception as e:
        logging.error(f"\nAn error occurred: {e}")
        print(f"\nError: {e}")
        print("Check the log file for more details.")
        input("Press Enter to exit...")
        raise
