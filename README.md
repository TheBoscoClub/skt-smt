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

## License

The code is licensed under GNU General Public License v3, making it free software that users can redistribute and modify.

See [LICENSE.txt](LICENSE.txt) for full GPL-3 license text.

## Legal Disclaimer

### Use at Your Own Risk

This software is provided "AS IS" without warranty of any kind, express or implied. The maintainer makes no representations or warranties regarding:
- Functionality or fitness for any particular purpose
- Compliance with any laws or regulations
- Freedom from errors or defects
- Safety or appropriateness for any specific use case

### Limited Liability

**The maintainer shall NOT be liable for:**
- Any damages arising from use or inability to use this software
- Any misuse of input simulation capabilities
- Any claims by third parties
- Any legal consequences of using this software
- Any system instability, data loss, or other technical issues

### User Responsibility

Users are solely responsible for:
- Using this software in compliance with all applicable laws and regulations
- Obtaining proper authorization before testing systems they do not own
- Understanding and accepting risks of input simulation software
- Not using this software for malicious purposes, unauthorized access, or fraudulent activities
- Ensuring use complies with organizational policies and acceptable use agreements

### Authorized Use Only

**This software must only be used for:**
- Testing applications you own or have explicit authorization to test
- Educational purposes in controlled environments
- Legitimate automation of your own systems
- Security research with proper authorization

**Prohibited uses include:**
- Unauthorized access to computer systems
- Circumventing security controls without authorization
- Fraudulent activity or deception
- Violating terms of service of any software or platform
- Any illegal activities

### No Security Guarantees

This tool:
- Does not guarantee perfect input simulation
- May be detectable by anti-automation systems
- Should not be relied upon for production automation
- Is intended for testing and development purposes only

### Input Simulation Risks

Users should be aware that:
- Input simulation can trigger unexpected system behaviors
- Simulated input may interact with system or application controls
- Testing should be performed in isolated, controlled environments
- The maintainer is not responsible for any unintended consequences

### Third-Party Systems

When using this software to test third-party systems or applications:
- Obtain explicit written authorization first
- Comply with all terms of service and acceptable use policies
- Document your authorized testing activities
- Respect system boundaries and limitations

### No Legal or Professional Advice

Nothing in this software or documentation constitutes legal, security, or professional advice. For specific guidance on authorized testing or compliance, consult qualified professionals.

### Indemnification

By using this software, you agree to indemnify and hold harmless the maintainer from any claims, damages, or legal issues arising from your use, including but not limited to:
- Unauthorized access or testing
- Violations of laws or regulations
- Breaches of terms of service
- Damages to systems or data
- Claims by third parties

### Testing Environment

Users are strongly encouraged to:
- Test only in isolated, non-production environments
- Have proper backups before testing
- Monitor system behavior during testing
- Stop immediately if unexpected behavior occurs
- Document all testing activities

## Ethical Use Statement

This software is provided for legitimate testing, development, and educational purposes. The maintainer condemns and does not support:
- Unauthorized access to computer systems
- Circumvention of security controls
- Fraudulent activities
- Any illegal or unethical use

Users are expected to use this software ethically, responsibly, and in compliance with all applicable laws and regulations.

---

**Platform**: Windows | **License**: GPL-3 | **Language**: Python
**Use Responsibly** • **Obtain Authorization** • **Test Ethically**
