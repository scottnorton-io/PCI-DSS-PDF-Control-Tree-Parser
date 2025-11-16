# Security Standards for PCI DSS PDF Control Tree Parser

This document outlines the minimum security expectations for working on
and with this repository.

## 1. Scope & Data Handling

- Do **not** process or store live cardholder data (CHD) or sensitive
  authentication data (SAD) with this tool.
- Only use the official PCI DSS v4.0.1 PDF or equivalent public
  documentation as input.

## 2. Development Practices

- Use a dedicated Python virtual environment (see `docs/DEV_WORKFLOW.md`).
- Avoid `sudo` with `pip`; dependencies should be isolated to the venv.
- Keep dependencies minimal and pinned via `requirements.txt`.

## 3. AI & Automation

- AI assistance may be used only for code and documentation drafting.
- All AI-generated content is considered **draft** until reviewed.
- Do not paste proprietary or confidential client data into AI prompts.

## 4. Verification & Review

- Treat parser output as support tooling, not a compliance oracle.
- Validate extracted requirements and structure against the canonical
  PCI DSS documentation.
