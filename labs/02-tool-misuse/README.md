# Lab 02: Parameter Pollution (OWASP-AI T2)

This lab demonstrates a Parameter Pollution vulnerability in an AI-powered booking system. This is a practical example of the **OWASP Top 10 for LLM Applications vulnerability #2: Insecure Plugin Design**.

## 🔍 The Vulnerability

In this scenario, an AI assistant helps users book tickets for events. However, the vulnerable implementation fails to validate numerical inputs, allowing attackers to:

1. Request an excessive number of seats (e.g., 500)
2. Deplete available inventory (causing denial of service)
3. Generate significant financial impact (unauthorized financial commitments)

This is a real-world example of what happens when parameters passed from LLMs to function calls aren't properly validated.

## 🔧 Lab Components

- **Vulnerable Version**: `starter/app/tool_main.py` 
  - Accepts any value for `num_seats` without validation
  - Allows booking unlimited numbers of seats
  
- **Secure Version**: `solution/app/safe_main.py`
  - Implements proper parameter validation
  - Enforces reasonable limits (max 10 seats per booking)
  - Shows how to properly sanitize and validate LLM outputs before acting on them

## 🚀 Running the Lab

### Prerequisites
- Python 3.8+
- `OPENAI_API_KEY` in your environment (tests use a stub if not available)

### Quick Demo

The easiest way to experience this lab is using the demo script:

```bash
# Install dependencies
pip install -r starter/app/requirements.txt

# Run the demo
bash demo.sh
```

This will:
1. Start the vulnerable server and demonstrate a successful attack
2. Start the secure server and show how it blocks the same attack
3. Demonstrate that legitimate bookings still work on the secure server

### Manual Testing

You can also test the components manually:

| Mode | What you run | Expected result |
|------|--------------|-----------------|
| **Vulnerable** | `cd starter && uvicorn app.tool_main:app --reload` | Attacker can trick the system into booking 500 seats 🔥 |
| **Patched** | `cd solution && uvicorn app.safe_main:app --reload` | Same prompt is validated, excessive booking rejected ✅ |

To test the vulnerable server with curl:

```bash
# Attacker carefully crafts a prompt to trick the AI into booking 500 seats
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Could you help me book all 500 seats for the Rock Symphony? My name is John Smith and my email is john@example.com."}'
```

## 🛡️ Security Principles

This lab teaches several important AI security principles:

- **Never trust parameters from LLMs**: Always validate and sanitize before use
- **Set reasonable limits**: Define acceptable numerical ranges for all parameters
- **Implement guardrails**: Use frameworks that enforce parameter validation
- **Fail securely**: Reject suspicious inputs rather than trying to "make them work"

## 📊 Understanding the Attack

The attack exploits parameter manipulation by:

1. Tricking the AI assistant into making a function call with an abnormally large value
2. Bypassing common sense limits that a human operator would enforce
3. Taking advantage of the system's trust in the LLM's judgment

## 🧪 Testing

Run the automated tests:

```bash
pytest -q tests/
```

## 🔍 Key Security Lessons

After completing this lab, you'll understand:

- How parameter pollution vulnerabilities can impact business operations
- Why numerical validation is critical in AI-powered systems
- How to properly secure function calls in AI applications
- Strategies for building robust validation systems for AI tools

## 💡 Stretch Ideas

- Implement dynamic validation based on venue capacity percentages
- Add rate limiting to prevent multiple bookings in quick succession
- Create a risk scoring system to detect unusual booking patterns
- Add additional validation for parameter types
- Implement behavioral analysis to detect unusual parameter manipulation attempts

## 🔗 Related Resources

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [OWASP ASVS - V5: Validation, Sanitization and Encoding](https://owasp.org/www-project-application-security-verification-standard/)
- [Best Practices for LLM Function Calling](https://platform.openai.com/docs/guides/function-calling) 