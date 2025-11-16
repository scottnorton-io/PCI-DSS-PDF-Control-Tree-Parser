# AI_ASSISTANT.md

## Purpose

This document defines how AI assistants (e.g., ChatGPT, Claude, GitHub Copilot) should interact with this repository.  
It sets expectations for code quality, documentation, architecture alignment, and security.

When using an AI assistant to generate or modify content in this repo, **follow these guidelines.**

---

## 1. General Behavior

- Prefer **clarity, safety, and maintainability** over cleverness.
- When in doubt, choose the **simpler, more explicit** implementation.
- Always explain non-trivial design decisions through comments or docstrings.
- Assume your output will be **reviewed by humans** and should be understandable.

---

## 2. Coding Standards

- Write **modular, reusable** code.
- Favor **small, composable functions** over large monoliths.
- Use **clear and descriptive names** for variables, functions, classes, and files.
- Avoid unnecessary global state and side effects.

### 2.1 Language-Specific Preferences

Adapt these rules to the languages present in the repo.

#### Python
- Use type hints where practical.
- Include docstrings using a consistent style (e.g., Google or NumPy).
- Prefer pathlib over hardcoded paths.
- Avoid OS-specific assumptions (use cross-platform APIs where possible).

#### JavaScript / TypeScript
- Prefer TypeScript interfaces/types when available.
- Use async/await instead of raw Promises for clarity.
- Keep functions small and focused.
- Validate and sanitize external input.

*(Adjust/extend this section to match the actual tech stack.)*

---

## 3. Architecture Alignment

- Before generating code, **consult `ARCHITECTURE.md`** to understand:
  - Key modules and their responsibilities
  - Expected data flows
  - Existing patterns for logging, error handling, and configuration
- Extend existing patterns instead of inventing new ones.

If `ARCHITECTURE.md` is missing or incomplete, propose improvements instead of guessing.

---

## 4. Error Handling & Logging

- Fail **loudly and clearly**, but not catastrophically:
  - Raise meaningful exceptions with context.
  - Do not swallow errors silently.
- Prefer **structured logging** (with consistent fields) over ad-hoc print statements.
- Never log sensitive data (passwords, tokens, secrets, card data, etc.).

If in doubt, **leave out** anything that might be sensitive.

---

## 5. Security Expectations

Even if this project is not explicitly “security-focused,” follow these default rules:

- **Validate all input**, especially anything external or user-controlled.
- Avoid constructing shell commands with unsanitized input.
- Use secure defaults for:
  - Cryptography libraries
  - HTTP clients
  - Authentication and session handling
- Do not hardcode secrets, API keys, or credentials. Use environment variables or secret stores.

If this project touches regulated data (e.g., payment info, PII), align with:

- Least privilege
- Strong access controls
- Proper logging and monitoring
- Defense-in-depth

If unsure whether something may have compliance impact, **flag it in comments** and in PR descriptions.

---

## 6. Documentation & Comments

- Include docstrings for public functions, classes, and complex logic.
- Use comments to explain **why**, not just **what**, for non-obvious decisions.
- Update documentation when changing behavior or interfaces.

---

## 7. AI Usage Patterns

When using an AI assistant in this repo:

1. Provide **enough context**: file contents, relevant snippets, `ARCHITECTURE.md` when needed.
2. Ask for **reasoning and alternatives**, especially for architectural changes.
3. Validate AI-generated code:
   - Run tests if they exist.
   - Add or update tests when you change behavior.
4. Prefer incremental changes (small PRs) over massive rewrites.

---

## 8. When Unsure

If the AI assistant is unsure about design, architecture, or domain-specific behavior, it should:

- Ask for more context, **or**
- Propose multiple options and clearly list tradeoffs.

The goal is to assist humans in making better decisions, not to guess silently.
