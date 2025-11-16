# Security Standards

This document defines baseline security expectations for this project.

---

## 1. General Principles

- Least privilege
- Defense in depth
- Fail securely
- Secure by default

---

## 2. Input Validation & Output Encoding

- Validate all external inputs.
- Sanitize or encode outputs appropriately for their destination.

---

## 3. Authentication & Authorization

If applicable:

- Use well-tested libraries.
- Centralize authorization checks.
- Protect administrative and sensitive operations.

---

## 4. Secrets Management

- Do not hardcode secrets.
- Use environment variables or secret management tools.
- Rotate exposed secrets as soon as possible.

---

## 5. Logging & Monitoring

- Log security-relevant events (auth, access controls, failures).
- Avoid logging sensitive data.
- Use consistent log formats where possible.

---

## 6. Cryptography

- Use standard cryptographic libraries.
- Avoid creating custom cryptocurrency or encryption algorithms.
- Follow recommended key sizes and configurations.

---

## 7. Dependencies

- Keep dependencies updated.
- Use vulnerability scanners or audits where available.

---

## 8. Reporting Issues

Document how to report suspected security issues to maintainers.
