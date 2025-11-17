## 1. Executive Summary

This repository is a single-purpose Python tool: it parses the official PCI DSS v4.0.1 PDF and turns the “Requirements and Testing Procedures” tables into a hierarchical control tree in YAML or JSON. The current structure is already clean and simple, with:

- `src/pci_dss_pdf_control_tree_parser/` – parser package
- `scripts/` – helper shell scripts
- `tests/` – basic unit tests
- Top-level docs like `README.md`, `AI_ASSISTANT.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `SECURITY_STANDARDS.md`, `DEV_WORKFLOW.md` and project files like `requirements.txt` and `rebuild.sh`. (GitHub)

The files below tighten everything into a coherent “AI-assisted but assessor-owned” story and give you reusable patterns you can drop into other PCI-related repos.

## 2. Support Files

You can treat each section below as a complete file to copy/paste into the repo.

### 🔹 AI_ASSISTANT.md

```markdown
# AI Assistant Guidelines – PCI DSS PDF Control Tree Parser

This document explains **how AI tools should interact with this repository**.

The goal:  
Use AI to accelerate development, *without* blurring the line between helpful automation and actual PCI DSS assessor judgment.

---

## 1. Role of the AI Assistant

The AI assistant acts as:

- **Application architect** – proposing structure, modularization, and refactors.
- **Documentation engineer** – drafting and improving README, architecture notes, and developer guides.
- **Code collaborator** – suggesting implementations, tests, and examples.

The AI assistant does **not**:

- Make PCI DSS compliance determinations.
- Define scope for PCI DSS assessments.
- Interpret this parser’s output as “evidence” without human review.

All AI-generated or AI-influenced content is **Draft – AI Generated** and must be reviewed by a human maintainer or assessor.

---

## 2. Coding Conventions

### 2.1 Style

- Follow **PEP 8** for Python style.
- Use **type hints** for all public functions and methods.
- Use **docstrings** for:
  - Modules
  - Classes
  - Public functions/methods

Example:

```python
def extract_spec_tables(doc: pdfplumber.PDF) -> list[list[list[str]]]:
    """
    Extract all tables from the PCI DSS PDF.

    Args:
        doc: A pdfplumber PDF object.

    Returns:
        A list of tables, where each table is a list of rows,
        and each row is a list of cell strings.
    """

```

### 2.2 Error Handling

- Prefer **explicit**, **predictable** errors:
  - Use `ValueError`, `RuntimeError`, or custom exceptions when appropriate.
  - Surface clear, human-friendly messages at the CLI layer.
- Do not silently swallow exceptions.
- For CLI:
  - Exit with `sys.exit(...)` and a short message.
  - Avoid printing stack traces unless `--debug` is explicitly requested.

### 2.3 Logging

Current tool is small enough to rely mostly on standard output, but as it grows:
- Use the standard logging module.
- Default level: INFO for normal usage, DEBUG when requested (e.g. --debug).
- Avoid logging sensitive information (paths are fine; secrets, tokens, or internal business data are not).

---

## 3. Architecture Expectations

The repository is organized as:
- `src/pci_dss_pdf_control_tree_parser/` – core parser package
- `scripts/` – shell helpers (e.g., `run_parser.sh`)
- `tests/` – pytest tests
- Root-level docs – `README.md`, `ARCHITECTURE.md`, `SECURITY_STANDARDS.md`, etc.

When the AI assistant adds or modifies functionality, it should:
- **Keep the core logic in** `src/pci_dss_pdf_control_tree_parser/`.
- **Use small, focused function** (single responsibility).
- **Avoid hardcoding file paths**:
  - Accept file paths via CLI arguments or function parameters.
  - Keep macOS/Linux portability in mind.
- **Maintain pure functions where possible**:
  - Functions that accept inputs and return outputs, without side effects, are easier to test and reuse.

---

## 4. Naming & Directory Standards
- Package name: `pci_dss_pdf_control_tree_parser`
  - Lowercase, underscore-separated.
- Filenames:
  - Descriptive and lowercase, e.g. `pci_dss_parser.py`, `cli.py`.
- Directories:
  - `src/` – source code
  - `tests/` – tests
  - `scripts/` – executable helper scripts
  - `docs/` (optional future consolidation) – narrative documentation

For any new modules:
- Place under `src/pci_dss_pdf_control_tree_parser/`.
- Consider a short prefix `pci_dss_` only if needed for clarity.

---

## 5. PCI DSS Coding References
While this tool processes **PCI DSS standard documents**, not cardholder data, the code should still follow **PCI DSS-friendly secure coding practices**, aligned with:
- Requirement 6: “Develop and maintain secure systems and software.”
- General secure coding expectations:
  - Avoid injection vulnerabilities.
  - Validate and sanitize inputs (even PDFs).
  - Fail safely with clear errors.
  - Keep dependencies minimal and maintained.
- Key principles to follow:
  - Never log or store CHD/SAD (even though this tool should never see them).
  - Treat all external input (including PDFs and future config files) as untrusted.
  - Use virtual environments and pinned dependencies.

---

## 6. AI Usage Patterns
### 6.1 Allowed
The AI assistant **may**:
- Draft new functions, classes, or modules.
- Propose refactors and reorganizations.
- Generate or improve documentation.
- Suggest tests and fixtures.
- Provide PCI DSS context so humans can better interpret output.

### 6.2 Not Allowed
The AI assistant must not:
- Assert that this repository, its code, or its outputs provide PCI DSS compliance.
- Embed secrets (API keys, tokens, passwords) into code or docs.
- Encourage copying proprietary PCI content beyond what’s permitted.

If in doubt: clearly label outputs as Draft – AI Generated and ask for human review.

---

## 7. AI Assistant Checklist (Before Proposing Changes)
When the AI assistant proposes changes, it should ensure:
- [ ] Code follows repo structure and naming conventions.
- [ ] Functions are typed and documented.
- [ ] No secrets or environment-specific paths are hardcoded.
- [ ] Any new behavior includes at least a basic test.
- [ ] All compliance-relevant language stresses draft and human review.

---

### 🔹 `ARCHITECTURE.md`

```markdown
# Architecture – PCI DSS v4.0.1 PDF Control Tree Parser

This document explains how the repository is organized, how the main components fit together, and where you can extend or adapt the tool.

---

## 1. High-Level Overview

**Purpose:**  
Parse the official PCI DSS v4.0.1 PDF and extract the “Requirements and Testing Procedures” content into a **structured, hierarchical control tree**.

**Core outputs:**

- **YAML** – with a standard control header and nested `controls`.
- **JSON** – simple hierarchy suitable for downstream tooling.

This project is intentionally small and focused so it can be reused inside larger PCI DSS automation ecosystems (evidence mapping, ROC drafting, index-building, etc.).

---

## 2. Repository Layout

At a high level:

- `src/pci_dss_pdf_control_tree_parser/`
  - Core parser code (currently `pci_dss_parser.py`).
- `scripts/`
  - `run_parser.sh` – helper script for invoking the parser with a venv.
- `tests/`
  - Basic pytest tests covering table parsing, requirement blob extraction, and tree building.
- Root files:
  - `README.md` – main project overview and quick start.
  - `AI_ASSISTANT.md` – AI collaboration contract.
  - `ARCHITECTURE.md` – this file.
  - `CONTRIBUTING.md` – workflow and contribution rules.
  - `SECURITY_STANDARDS.md` – secure usage and development expectations.
  - `DEV_WORKFLOW.md` or equivalent – macOS/venv setup guide.
  - `requirements.txt` – Python dependency pinning.
  - `rebuild.sh` / scripts – convenience wrappers.
  - (Optional) `PCI-DSS-PDF-Control-Tree-Parser-full.zip` – snapshot bundle.

---

## 3. Core Components

### 3.1 `ComplianceControlNode`

**Location:** `src/pci_dss_pdf_control_tree_parser/pci_dss_parser.py`

Represents a single PCI DSS requirement node.

Key fields:

- `id`: Parsed requirement ID (e.g., `1`, `1.2`, `1.2.3`, `A1.1.1`).
- `title`: Cleaned title line extracted from the “Requirements and Testing Procedures” text.
- `raw_blob`: Full concatenated text from the PDF table.
- `children`: Child requirements, forming the hierarchy.
- `parent` / `depth`: Relationship and position in the tree.

**Responsibilities:**

- Parse out the requirement ID using a regex (`REQ_INDEX_PATTERN`).
- Normalize the title by stripping trailing notes / bullets via `title_split_patterns`.
- Provide a JSON-serializable `to_dict()` method used by JSON output.

---

### 3.2 `ComplianceControlTree`

**Location:** same module as above.

A thin orchestrator that:

- Holds a synthetic `root` node.
- Uses the **depth of the requirement ID** (number of segments) to decide where each node attaches:
  - `1` → depth 1
  - `1.1` → depth 2, child of `1`
  - `1.1.1` → depth 3, child of `1.1`, etc.
- Maintains a mapping `last_by_depth` so it can attach new nodes to the appropriate parent as it walks the requirement list.

Outputs:

- `to_dict()` returns a list of top-level children (root requirements), suitable for JSON.

---

### 3.3 `YamlFormatter`

Responsible for turning the tree into a **YAML control file** with a PCI-style header.

Capabilities:

- Emits a fixed header containing:
  - `policy`, `title`, `id`, `version`, and `source`.
  - `levels` list with a base level.
- Walks the `ComplianceControlTree` nodes depth-first.
- For each node:
  - Writes `- id: Req-<requirement id>`.
  - Writes a wrapped `title` line with indentation.
  - Adds `levels`, `status`, and either `controls:` or `rules: []`.

This output is intentionally compatible with downstream tools that expect a hierarchical control list.

---

### 3.4 PDF & Table Extraction Helpers

**Key helpers:**

- `extract_spec_tables(pdfdoc)`
  - Uses `pdfplumber` to extract tables from all pages.
- `find_requirements_column_index(table)`
  - Looks for the column whose header contains “Requirements and Testing Procedures”.
- `update_list_req(list_req, req_index, cell)`
  - Builds up text blobs:
    - Starts new blob when a cell begins with a requirement ID.
    - Appends to the previous blob when it’s the continuation of the same requirement.
- `extract_requirement_blobs(tables)`
  - Loops over all tables and collects all requirement blobs for feeding into `ComplianceControlTree`.

---

### 3.5 CLI Interface (`main()`)

The CLI layer:

- Parses CLI arguments:
  - `pdf` path
  - `--format` (`yaml` or `json`)
  - `--output` file (optional)
- Validates the input PDF path.
- Calls table extraction helpers, then builds the tree.
- Outputs:
  - YAML (default) via `YamlFormatter`  
  - JSON via `json.dumps(tree.to_dict())`

Errors are handled with clear `sys.exit(...)` messages.

---

## 4. Textual Data Flow Diagram

Think of the end-to-end flow as:

1. **User CLI**  
   `python -m pci_dss_pdf_control_tree_parser.pci_dss_parser PCI-DSS-v4_0_1.pdf -f yaml -o controls.yaml`

2. **PDF Loader**  
   `pdfplumber.open(pdf_path)` → returns PDF object.

3. **Table Extraction**  
   `extract_spec_tables(pdfdoc)` → returns list of tables (rows + cells).

4. **Column Filtering**  
   For each table:  
   `find_requirements_column_index(table)` → locate the “Requirements and Testing Procedures” column.

5. **Requirement Blob Building**  
   `extract_requirement_blobs(tables)` → `[ "1 ...", "1.1 ...", "1.1.1 ...", ... ]`

6. **Tree Build**  
   For each blob: `ComplianceControlTree.add_node_from_blob(blob)`  
   → Node gets an ID and title, attaches to parent based on ID depth.

7. **Rendering**  
   - YAML: `YamlFormatter(tree.root).format()`  
   - JSON: `json.dumps(tree.to_dict(), indent=2)`  

8. **Output**  
   - Write to disk via `--output`
   - Or print to stdout.

---

## 5. Future Improvements

Some future directions if you want to expand the tool:

1. **Support for Additional PCI Artifacts**
   - Parse other official PDFs (e.g., SAQ instructions, ROC templates) in separate modules.
   - Extend structures to include testing procedures separately alongside requirement titles.

2. **Configurable Header & Metadata**
   - Allow users to provide a YAML or JSON template for header fields (policy name, version, etc.).

3. **Rich Logging**
   - Add optional `--debug` flag and structured logging to trace parsing issues.

4. **Pluggable Output Formats**
   - Export to:
     - CSV (flat list)
     - Notion import JSON
     - Vanta / Fieldguide / other GRC schemas.

5. **Robust Testing on Real PDFs**
   - Include anonymized fixtures or checksums to verify that changes don’t break parsing across PCI DSS PDF minor revisions.

---

## 6. Scaling & Integration Guidance

This tool is intentionally simple, but can scale in two directions:

- **Horizontally** – Integrate with other repos (e.g., PCI DSS article series, policy automation, data indexers) as a component in a larger pipeline.
- **Vertically** – Add more parsing layers:
  - Testing procedures
  - Applicability notes
  - Customized approach objectives

When integrating into larger systems or pipelines:

- Treat this parser as a **pure transformation step**:
  - Input: official PCI DSS PDF.
  - Output: structured requirements data.
- Keep orchestration, storage, and further processing outside this repo.

```

### 🔹 `CONTRIBUTING.md`

```markdown
# Contributing Guide – PCI DSS PDF Control Tree Parser

Thank you for taking the time to contribute. This project is small on purpose, but it sits in a bigger PCI DSS ecosystem, so clarity and discipline really matter.

---

## 1. Ground Rules

- **No CHD/SAD, ever.**  
  Do not commit, paste, or otherwise introduce any cardholder data (CHD) or sensitive authentication data (SAD) into this repository.

- **No compliance guarantees.**  
  This project is a helper tool, not a compliance oracle. Do not represent it as providing PCI DSS “compliance.”

- **Human review is mandatory.**  
  All outputs and AI-assisted artifacts are **Draft – AI Generated** until reviewed by a human.

For secure development and PCI-relevant expectations, see `SECURITY_STANDARDS.md`.

---

## 2. Branching Strategy

- Default branch: `main`
- Recommended approach:
  - `feature/<short-description>` for new features.
  - `fix/<short-description>` for bugfixes.
  - `docs/<short-description>` for documentation-only changes.

Example:

- `feature/add-json-pretty-print`
- `fix/handle-missing-tables`
- `docs/improve-architecture-notes`

---

## 3. Code Style & Testing

### 3.1 Python Style

- Follow **PEP 8**.
- Use **type hints** for all new or modified public functions.
- Add **docstrings** describing the function, arguments, and return values.
- Avoid global state where possible; prefer dependency injection via function arguments.

### 3.2 Virtual Environment

Use a per-repo venv:

```bash

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

```

### 3.3 Tests
- Use **pytest**.
- Place tests in the `tests/` directory.
- Name test files `test_*.py`.
- Run tests before opening a PR:
```bash

pytest

```
If you add a new behavior, add or update tests that exercise it.

---

## 4. Commit Message Conventions

Use clear, action-oriented messages. Conventional Commits style is welcome but not required.

Good examples:
- `feat: support JSON output`
- `fix: handle missing requirements column`
- `docs: clarify macOS venv setup`
- `test: add coverage for A1.* requirements`

Avoid vague messages like `update` or `misc changes`.

---

## 5. Pull Request Workflow
1. **Fork* the repository (if you don’t have write access).
2. **Create a branch** for your change.
3. *8Implement your changes**, update tests and docs.
4. **Run tests** locally to ensure they pass.
5. **Open a Pull Request**:
  -Describe what changed and why.
   Note any breaking changes.
   Mention whether you used AI assistance.

PR checklist:
- [ ] Code follows style and type-hinting guidelines.
- [ ] Tests pass locally (`pytest`).
- [ ] No CHD/SAD or proprietary client data is introduced.
- [ ] Documentation has been updated if behavior changed.
- [ ] AI-assisted content is clearly understood and verified by you.

---

## 6. AI Assistant Guidelines
If you use an AI assistant (including the one documented in `AI_ASSISTANT.md`):
- You are responsible for:
  - Understanding the code it suggests.
  - Verifying that it matches project standards.
  - Ensuring no sensitive data was shared with the AI.

When you open a PR:
- It’s helpful to note:
  `This change was drafted with AI assistance and fully reviewed by the author.`

For more details, see `AI_ASSISTANT.md`.

---

## 7. How to Ask for Help
If you’re not sure how to approach a change:
- Open a GitHub Issue describing:
  - The problem you’re trying to solve.
  - Any ideas you already have.
- Keep it conversational and practical. This repo is meant to be approachable, not intimidating.
```

---

### 🔹 `SECURITY_STANDARDS.md`

```markdown
# Security & Compliance Standards – PCI DSS PDF Control Tree Parser

Even though this tool only parses **public PCI DSS documentation**, we treat its development with the same seriousness we’d expect from PCI-related tooling.

This document lays out security expectations for contributors and users.

---

## 1. Scope & Data Handling

- This tool is designed to process **official PCI DSS v4.x standard PDFs**.
- It is **not** designed to process:
  - Cardholder Data (CHD)
  - Sensitive Authentication Data (SAD)
  - Client-specific logs or evidence artifacts

**Do not**:

- Point this tool at production evidence repositories.
- Feed it PDFs or documents containing live PANs, track data, CVV, or other sensitive data.

---

## 2. Secure Development Practices

### 2.1 Dependencies

- Keep dependencies minimal and explicit in `requirements.txt`.
- When updating dependencies:
  - Prefer compatible, stable versions.
  - Avoid unmaintained or suspicious packages.

### 2.2 Virtual Environments

- Always use a virtual environment (e.g., `.venv`) to isolate dependencies.
- Do not install this project’s dependencies into your system Python with `sudo`.

### 2.3 Secrets Management

- This tool does not require API keys, tokens, or other secrets.
- If you extend it to integrate with other systems:
  - Do **not** hardcode secrets in code or configuration.
  - Use environment variables or OS keychains (for example, macOS Keychain).
  - Add `.env`-style environment files to `.gitignore`.

---

## 3. Logging & Error Handling

Because this tool operates on public standard documents, logging risk is low—but we still follow safe patterns:

- Log high-level status information (e.g., “starting parse”, “tables found: N”).
- Avoid logging full content of PDFs or large internal structures unless necessary for debugging.
- For CLI errors:
  - Provide clear, short messages like:
    - `Error: PDF not found at path: ...`
    - `No tables found in the PDF.`
  - Use non-zero exit codes via `sys.exit()`.

If the tool is ever extended to work with customer input or evidence:

- Review logging to ensure no sensitive data is written to disk, stdout, or external logging systems.

---

## 4. PCI DSS Alignment

This repository is **not** a PCI DSS system in itself, but we align with key principles:

- **Requirement 3 & 4** – No CHD/SAD is stored, transmitted, or processed by this tool by design.
- **Requirement 6** – We follow secure coding practices:
  - Clear input validation and error handling.
  - Minimal attack surface (small dependency set, no network calls by default).
  - Regular review of dependencies and code.
- **Requirement 10** – If integrated into a larger pipeline, logging and audit trails should be managed by that pipeline.

---

## 5. AI & Compliance

AI can accelerate development, but:

- AI-generated code and docs are **drafts**, not final.
- No AI output should be treated as a compliance determination, scope definition, or assessor conclusion.
- Do not paste proprietary client data or confidential evidence into AI prompts.

For detailed AI collaboration guidance, see `AI_ASSISTANT.md`.

---

## 6. Verification & Review

- Treat parser output as a **starting point** for automation, not a substitute for reading the actual PCI DSS standard.
- Periodically:
  - Re-run the parser against the latest official PCI DSS v4.x PDFs.
  - Spot check output against the canonical documents.
- If PCI SSC publishes a new minor version (e.g., v4.0.2), validate that:
  - Table structures are still compatible.
  - Requirement IDs and text are being parsed correctly.

When in doubt, the official PCI Security Standards Council documentation is the single source of truth.

```

---

🔹 Enhanced README.md

```markdown
# PCI DSS v4.0.1 PDF Control Tree Parser

This repository contains a focused Python tool that parses the **official PCI DSS v4.0.1 standard PDF** and converts the “Requirements and Testing Procedures” tables into a **hierarchical control tree** in YAML or JSON.

The goal is simple:  
Give assessors, advisors, and engineers a structured dataset they can plug into their own tools for mapping, indexing, or narrative generation — without pretending to be a compliance engine.

> **AI Use Disclosure**  
> We may use AI-assisted tools to help draft code and documentation.  
> These tools never make compliance determinations.  
> All outputs are reviewed and validated by a qualified assessor.

---

## ✅ What This Tool Does

- Reads the PCI DSS v4.0.1 PDF with `pdfplumber`.
- Locates the **“Requirements and Testing Procedures”** column in each table.
- Concatenates requirement text into clean “blobs.”
- Derives a requirement ID (e.g., `1`, `1.1`, `1.1.1`, `A1.1.1`) for each blob.
- Builds a hierarchical tree using ID depth (1 → 1.1 → 1.1.1, etc.).
- Outputs:
  - **YAML** with a PCI-style header and nested `controls`.
  - **JSON** representing the same tree for downstream automation.

What it **does not** do:

- It does *not* provide PCI DSS compliance status.
- It does *not* interpret or validate your environment.
- It does *not* replace a qualified assessor.

---

## 🧩 Repository Layout

- `src/pci_dss_pdf_control_tree_parser/`
  - `pci_dss_parser.py` – main parser module (CLI + parsing + formatting).
- `scripts/`
  - `run_parser.sh` – convenience script for running the parser inside a venv.
- `tests/`
  - `test_parser_basic.py` – basic coverage for blob extraction and tree building.
- Top-level docs:
  - `README.md` – this file.
  - `AI_ASSISTANT.md` – guidelines for AI-assisted development.
  - `ARCHITECTURE.md` – detailed component and data flow description.
  - `CONTRIBUTING.md` – how to contribute safely and consistently.
  - `SECURITY_STANDARDS.md` – secure usage and PCI-aligned expectations.
  - `DEV_WORKFLOW.md` – macOS-friendly virtual environment setup.

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/scottnorton-io/PCI-DSS-PDF-Control-Tree-Parser.git
cd PCI-DSS-PDF-Control-Tree-Parser
```

### 2. Create and Activate a Virtual Environment (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Parser (YAML Output)

```bash
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /absolute/path/to/PCI-DSS-v4_0_1.pdf \
  -f yaml \
  -o controls.yaml
```

Or use the helper script:

```bash
./scripts/run_parser.sh /absolute/path/to/PCI-DSS-v4_0_1.pdf yaml controls.yaml
```

### 4. JSON Output Example

```bash
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /absolute/path/to/PCI-DSS-v4_0_1.pdf \
  -f json \
  -o controls.json
```

## 📄 Output Shape

**YAML (simplified)**
```yaml
---
policy: PCI-DSS
title: Configuration Recommendations of a GNU/Linux System
id: pcidss_4
version: '4'
source: https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf
levels:
  - id: base
controls:
  - id: Req-1
    title: 'Install and maintain network security controls.'
    levels:
      - base
    status: not applicable
    controls:
      - id: Req-1.1
        title: 'Network security controls are documented and implemented...'
        levels:
          - base
        status: not applicable
        controls:
          - id: Req-1.1.1
            title: 'Firewall configuration standards are established and reviewed...'
            levels:
              - base
            status: not applicable
            rules: []
```

**JSON (simplified)**
```json
[
  {
    "id": "1",
    "title": "Install and maintain network security controls.",
    "children": [
      {
        "id": "1.1",
        "title": "Network security controls are documented and implemented...",
        "children": [
          {
            "id": "1.1.1",
            "title": "Firewall configuration standards are established and reviewed...",
            "children": []
          }
        ]
      }
    ]
  }
]
```
> Note: Titles above are illustrative; actual output depends on the official PCI DSS PDF text and parsing rules.

## 🧪 Testing
With your virtual environment active:

```bash
pytest
```

This will run basic tests around:
- Locating the requirements column.
- Extracting requirement blobs.
- Building parent/child relationships (e.g., 1 → 1.1 → 1.1.1).

As you add functionality, extend the tests in `tests/` to cover new behavior.

## 🔐 Security & Compliance Notes
- This tool is intended for public **PCI DSS standard documents only**.
- Do not use it directly on:
  - Evidence PDFs containing CHD/SAD.
  - Client-specific internal documents that include cardholder data.
- All parser outputs are draft artifacts; they must be reviewed and validated by a qualified assessor before being used in any ROC, AOC, or client deliverable.

For details, see `SECURITY_STANDARDS.md`.

## 🤝 Contributions & AI Collaboration

Contributions are welcome.
- See `CONTRIBUTING.md` for:
  - Branching model
  - Code style
  - Testing and PR checklist
- See `AI_ASSISTANT.md` for:
  - How AI can be safely used as a co-pilot.
  - Coding and documentation expectations for AI-assisted changes.

If you open a PR with AI-assisted changes, just note it in the description and confirm you’ve reviewed and tested the results.

### 📌 Status Metadata (For Downstream Use)

If you consume this tool’s output in other systems, it’s helpful to track:
```plaintext

status: "Draft – AI Generated"
reviewer: "TBD"
validation_date: "TBD"
source_reference: "PCI-DSS-v4.0.1-PDF-Parser"

```

This keeps the “AI-assisted, assessor-validated” boundary explicit.

### ⚠️ Disclaimer
This repository and its maintainers:
- Do **not** provide legal, regulatory, or PCI DSS compliance advice.
- Do **not** guarantee that the output is correct, complete, or sufficient for any assessment.
- Provide this tool strictly as a helper for professionals who remain responsible for their own PCI DSS interpretations and decisions.

---

## 3. Repo Improvement Recommendations

A few targeted tweaks that will make this repo even more reusable and consistent:

1. **Consolidate documentation under `/docs` (optional)**
   - Move `DEV_WORKFLOW.md`, `ARCHITECTURE.md`, `AI_ASSISTANT.md`, `SECURITY_STANDARDS.md` into a `docs/` directory and update links in `README.md`.
   - This keeps the root tidy while still surfacing docs clearly.

2. **Add a `pyproject.toml` (future)**
   - To support modern tooling and packaging, consider adding a minimal `pyproject.toml` that:
     - Declares the package name (`pci_dss_pdf_control_tree_parser`).
     - Lists dependencies.
     - Makes it installable as a local package.

3. **Expose a Tiny Entry-Point Script (future)**
   - Add a `console_scripts` entry point (e.g., `pci-dss-pdf-parse`) so people can install and run it globally:
     - `pci-dss-pdf-parse PCI-DSS-v4_0_1.pdf -f yaml -o controls.yaml`

4. **Expand Tests Around Realistic Edge Cases**
   - Add tests for:
     - Requirements with alphabetic prefixes (`A1.1`, `A2.2.1`).
     - Tables without the target column (ensure graceful handling).
     - PDFs with slight header variations (“Requirements & Testing Procedures (cont.)”).

5. **Optional Notion / GRC Export Examples**
   - In a separate doc or example script, show:
     - How to take the JSON output and transform it into:
       - Notion import JSON
       - Vanta / Fieldguide dataset stubs

```
