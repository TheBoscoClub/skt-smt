# Safe Keyboard & Mouse Tester (SKT-SMT)

[![CodeFactor](https://www.codefactor.io/repository/github/theboscoclub/skt-smt/badge)](https://www.codefactor.io/repository/github/theboscoclub/skt-smt)

**License**: GPL-3 | **Platform**: Windows | **Language**: Python
**Dependencies**: Python 3.x, pywin32, Windows API
**Features**: Isolated input simulation, realistic typing patterns, human-like mouse physics, resource monitoring

### Version History

| Version | Status | Release |
|---------|--------|---------|
| ![1](https://img.shields.io/badge/1-brightgreen)![7](https://img.shields.io/badge/7-darkgreen)![1](https://img.shields.io/badge/1-green)![1](https://img.shields.io/badge/1-yellow) | Latest tweak | [v1.7.1.1](https://github.com/TheBoscoClub/skt-smt/releases/tag/v1.7.1.1) |
| ![1](https://img.shields.io/badge/1-brightred)![7](https://img.shields.io/badge/7-darkred)![1](https://img.shields.io/badge/1-red) | Prior patch | [v1.7.1](https://github.com/TheBoscoClub/skt-smt/releases/tag/v1.7.1) |
| ![1](https://img.shields.io/badge/1-brightred)![7](https://img.shields.io/badge/7-darkred)![0](https://img.shields.io/badge/0-red) | Prior minor | [v1.7.0](https://github.com/TheBoscoClub/skt-smt/releases/tag/v1.7.0) |

<details>
<summary>Badge Color Convention</summary>

Each segment: `brightgreen → darkgreen → green → yellow` (current) / `brightred → darkred → red → orange` (prior)

</details>

---

## Overview

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

## References & Related Projects

### Input Simulation Tools
- **PyAutoGUI**: [pyautogui.readthedocs.io](https://pyautogui.readthedocs.io/) - Cross-platform GUI automation
- **AutoHotkey**: [autohotkey.com](https://www.autohotkey.com/) - Scripting language for Windows automation
- **Selenium**: [selenium.dev](https://www.selenium.dev/) - Browser automation framework
- **Robot Framework**: [robotframework.org](https://robotframework.org/) - Generic test automation framework

### Windows API Resources
- **Windows API Documentation**: [Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/) - Official Windows API reference
- **PyWin32 Documentation**: [pywin32.readthedocs.io](https://pywin32.readthedocs.io/) - Python extensions for Windows
- **Win32 SendInput**: [Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput) - Input simulation API

### Testing & QA Resources
- **OWASP Testing Guide**: [owasp.org/testing](https://owasp.org/www-project-web-security-testing-guide/) - Security testing methodologies
- **Software Testing Help**: [softwaretestinghelp.com](https://www.softwaretestinghelp.com/) - Testing tutorials and guides
- **Ministry of Testing**: [ministryoftesting.com](https://www.ministryoftesting.com/) - Testing community and resources

### UI/UX Testing Tools
- **TestComplete**: [smartbear.com/testcomplete](https://smartbear.com/product/testcomplete/) - Commercial UI testing tool
- **Ranorex**: [ranorex.com](https://www.ranorex.com/) - Test automation platform
- **WinAppDriver**: [github.com/microsoft/WinAppDriver](https://github.com/microsoft/WinAppDriver) - Windows Application Driver

### Security Testing Resources
- **PTES - Penetration Testing Execution Standard**: [pentest-standard.org](http://www.pentest-standard.org/) - Penetration testing methodology
- **NIST Cybersecurity Framework**: [nist.gov/cyberframework](https://www.nist.gov/cyberframework) - Security standards and guidelines
- **CIS Controls**: [cisecurity.org/controls](https://www.cisecurity.org/controls) - Cybersecurity best practices

### Human-Computer Interaction
- **Fitts's Law**: [Wikipedia](https://en.wikipedia.org/wiki/Fitts%27s_law) - Model of human movement for UI design
- **Nielsen Norman Group**: [nngroup.com](https://www.nngroup.com/) - UX research and consulting
- **HCI Bibliography**: [hcibib.org](https://hcibib.org/) - Human-Computer Interaction resources

### Legal & Compliance
- **Computer Fraud and Abuse Act (CFAA)**: [justice.gov](https://www.justice.gov/criminal-ccips/computer-fraud-and-abuse-act) - U.S. computer crime law
- **GDPR**: [gdpr.eu](https://gdpr.eu/) - European data protection regulation
- **Responsible Disclosure**: [CERT Guide](https://vuls.cert.org/confluence/display/CVD) - Vulnerability disclosure best practices

### Community & Support
- **r/softwaretesting**: [reddit.com/r/softwaretesting](https://www.reddit.com/r/softwaretesting/)
- **r/QualityAssurance**: [reddit.com/r/QualityAssurance](https://www.reddit.com/r/QualityAssurance/)
- **Stack Overflow - Testing**: [stackoverflow.com/questions/tagged/testing](https://stackoverflow.com/questions/tagged/testing)

### Python Resources
- **Python Official Documentation**: [docs.python.org](https://docs.python.org/3/)
- **Real Python**: [realpython.com](https://realpython.com/) - Python tutorials and guides
- **PyPI**: [pypi.org](https://pypi.org/) - Python Package Index

---

**Platform**: Windows | **License**: GPL-3 | **Language**: Python
**Use Responsibly** • **Obtain Authorization** • **Test Ethically**
