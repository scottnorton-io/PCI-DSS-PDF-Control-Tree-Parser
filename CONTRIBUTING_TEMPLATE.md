# Contributing Guide

Thank you for your interest in contributing! This document explains how we work, how to propose changes, and how to keep the project healthy and maintainable.

---

## 1. Code of Conduct

By participating in this project, you agree to treat others with respect and professionalism.

---

## 2. Getting Started

1. Fork the repository.
2. Clone your fork.
3. Install dependencies.
4. Run tests to ensure everything is working.

Adapt the exact commands to match the project’s language and tooling.

---

## 3. Branching Strategy

Use a simple, clear branching model:

- `main` — stable, deployable branch.
- Feature branches — `feature/short-description`
- Bugfix branches — `fix/short-description`

---

## 4. Commit Messages

Use clear, descriptive commit messages. Example prefixes:

- `feat: ...`
- `fix: ...`
- `docs: ...`
- `test: ...`
- `refactor: ...`

---

## 5. Pull Requests

When opening a pull request:

- Ensure tests pass.
- Include or update tests for new behavior.
- Update documentation where necessary.
- Provide a clear description of what changed, why, and how to validate it.

---

## 6. Coding Style

- Follow the existing style and conventions in the codebase.
- Respect linter and formatter rules if configured.
- Avoid introducing new patterns if established ones exist.

---

## 7. AI Assistant Guidelines

If you use an AI assistant while contributing:

- Treat AI-generated code like code from a junior teammate.
- Review for security, performance, and maintainability.
- Ensure AI follows the guidance in `AI_ASSISTANT.md`.
- Do not commit secrets or sensitive values.

---

## 8. Security and Compliance

For changes involving authentication, authorization, data handling, or other sensitive areas:

- Reference `SECURITY_STANDARDS.md` if present.
- Call out any security-relevant changes in the PR description.
- Avoid logging or exposing sensitive data.

---

## 9. Questions?

If you are unsure about anything, please open an issue or a draft pull request for discussion.
