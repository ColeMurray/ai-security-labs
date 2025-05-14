# OWASP AI Security Labs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive collection of hands-on labs for learning and teaching practical AI security concepts based on the [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

## 🛡️ Overview

The OWASP AI Security Labs project provides practical, interactive exercises to help security professionals, developers, and AI practitioners understand and mitigate common vulnerabilities in AI systems, particularly Large Language Models (LLMs). Each lab focuses on a specific vulnerability from the OWASP AI Top 10, with clear examples demonstrating both the vulnerability and its remediation.

## 🔬 Labs

| Lab | Topic | OWASP AI Category | Description |
|-----|-------|-------------------|-------------|
| 01 | [Memory Poisoning](labs/01-memory-poisoning/) | LLM01: Prompt Injection | Learn how attackers can manipulate an AI's memory context to extract sensitive information |
| 02 | [Parameter Pollution](labs/02-tool-misuse/) | LLM02: Insecure Plugin Design | Explore how malicious inputs can bypass validation to cause system damage through tool function calls |

Each lab contains:
- A vulnerable implementation demonstrating the security issue
- A secure implementation showing proper mitigation techniques
- Detailed explanations and step-by-step instructions
- Interactive demos to experience the vulnerability firsthand

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key (for running the LLM interactions)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/ColeMurray/ai-security-labs.git
   cd ai-security-labs
   ```

2. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. Choose a lab and follow its README instructions:
   ```bash
   cd labs/01-memory-poisoning  # or any other lab
   # Follow the lab-specific instructions
   ```

## 📋 Lab Structure

Each lab follows a consistent structure:

- **README.md** - Instructions and explanations of the vulnerability
- **starter/** - Vulnerable code that demonstrates the security issue
- **solution/** - Fixed code with proper security controls
- **demo.sh** - Script to quickly demonstrate the vulnerability and fix

## 🤝 Contributing

Contributions are welcome! If you'd like to add a new lab, improve existing ones, or fix bugs, please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [AI Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [OWASP AI Security Project](https://owasp.org/www-project-ai-security-and-privacy-guide/)

## 🙏 Acknowledgments

- OWASP Foundation
