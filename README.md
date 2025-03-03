Overview of the Suite
This is a software package that allows you to simulate realistic human-like keyboard and mouse input without actually affecting other applications running on the system. It's useful for testing applications, automating repetitive tasks, or for any scenario where you need to generate input events that mimic human behavior.
Key Components

BaseInputTester (base_input_tester_1.7.py):

A foundation class that handles common functionality like window management, message processing, resource monitoring, and logging.
It provides the infrastructure that both the keyboard and mouse testers build upon.


SafeKeyboardTester (skt-1.7.py):

Simulates keyboard input with realistic typing patterns.
Can generate common words, random words, sentences, code snippets, and number sequences.
Implements human-like typing behaviors including variable speeds, occasional typos with corrections, and special key presses.


SafeMouseTester (smt-1.7.py):

Simulates mouse movements, clicks, and scrolling.
Supports different movement patterns (random, linear, circular, targeted).
Implements realistic mouse physics including acceleration/deceleration and natural curves.



How It Works
The tools work by creating special transparent or hidden windows that capture input events without interfering with other applications. They use Windows API functions to simulate keyboard and mouse events, with sophisticated algorithms to make the input patterns appear natural and human-like.
The tools are highly configurable through JSON configuration files, allowing you to adjust timing intervals, probabilities for different behaviors (like typos or clicks), and many other parameters.
Use Cases
This suite might be useful for:

Testing applications that process user input
Creating automated demos or tutorials
Stress-testing UI elements with realistic user interactions
Generating activity patterns for monitoring or security testing
Developing or testing input handling code

Key Features

Isolation: Simulates input without affecting other applications
Realism: Creates human-like input patterns with natural variations
Configurability: Extensive options for customizing behavior
Resource Management: Built-in monitoring to prevent memory leaks
Detailed Logging: Records all activities for analysis

The code is licensed under GNU General Public License v3, making it free software that users can redistribute and modify.
