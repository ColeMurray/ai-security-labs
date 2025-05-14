# Contributing to OWASP AI Security Labs

Thank you for your interest in contributing to the OWASP AI Security Labs project! This document provides guidelines and instructions for contributing.

## How to Contribute

There are several ways you can contribute to this project:

1. **Add a new lab**: Create a complete lab that demonstrates an AI security vulnerability
2. **Improve existing labs**: Enhance existing labs with better explanations, code, or demos
3. **Fix bugs**: Identify and fix issues in existing labs
4. **Documentation**: Improve READMEs, comments, and other documentation
5. **Testing**: Create or improve tests that validate the labs work as expected

## Creating a New Lab

To add a new security lab:

1. Follow the established directory structure:
   ```
   labs/
   ├── XX-lab-name/
   │   ├── README.md          # Lab instructions and explanations
   │   ├── starter/           # Vulnerable code
   │   │   └── app/
   │   │       ├── main.py
   │   │       └── requirements.txt
   │   ├── solution/          # Fixed code
   │   │   └── app/
   │   │       └── main.py
   │   ├── tests/             # Tests that verify the vulnerability and fix
   │   └── demo.sh            # Script to demonstrate the lab
   ```

2. Ensure your lab covers a specific OWASP AI security issue
3. Include clear instructions in the README
4. Provide working code for both the vulnerable and fixed versions
5. Create a demonstration script that clearly shows the problem and solution
6. Add appropriate tests

## Pull Request Process

1. Fork the repository
2. Create a feature branch from `main`
3. Make your changes
4. Test your changes thoroughly
5. Submit a pull request with a clear description of your changes

When submitting a PR, please:
- Explain what issue it addresses
- Describe how your changes fix the issue
- Note any dependencies that were added
- Reference any related issues or PRs

## Code Style

- Follow PEP 8 for Python code
- Include docstrings for all functions and classes
- Use clear, descriptive variable and function names
- Add comments explaining complex or non-obvious code

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the project's MIT license.

## Questions?

If you have questions about contributing, please open an issue in the repository with your question.

Thank you for helping make AI systems more secure! 