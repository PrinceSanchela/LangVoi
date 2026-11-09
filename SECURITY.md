# Security Policy — LangVoi Voice Studio Pro

Prince Sanchela and the LangVoi project take software security and acoustic privacy seriously.

---

## 🔒 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.2.x   | :white_check_mark: |
| < 2.2   | :x:                |

---

## 🛡️ Reporting a Vulnerability

If you discover a potential security vulnerability within **LangVoi Voice Studio Pro**, please do **NOT** open a public issue on GitHub. Instead, report it privately to the maintainer:

- **Lead Architect**: Prince Sanchela
- **Email**: `contact.princesanchela@gmail.com`
- **Security Response Target**: Within 48 hours

Please provide:
1. A clear description of the vulnerability.
2. Steps to reproduce or proof-of-concept.
3. Affected operating system version and Python runtime.

---

## 🗝️ Code Signing & Key Security Best Practices

- **Private Key Isolation**: Private Authenticode signing keys (`*.pfx`, `*.key`) are strictly git-ignored and never committed to source control.
- **Verification**: Public releases are cryptographically signed to ensure binary integrity and prevent tampering.
- **Zero Spyware**: LangVoi does not harvest user audio, track personal identifiers, or record keystrokes.
