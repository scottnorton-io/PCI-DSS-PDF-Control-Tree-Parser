# Architecture – PCI DSS PDF Control Tree Parser

## Overview

The parser extracts requirement data from the PCI DSS v4.0.1 PDF and
converts it into a hierarchical control tree structure for further
automation and reporting.

## Components

- **`ComplianceControlNode`**  
  Represents an individual PCI DSS requirement with:
  - `id` – Parsed requirement identifier (e.g., `1.1.1`, `A2.1.2`).
  - `title` – A cleaned, single-line title derived from the
    "Requirements and Testing Procedures" text.
  - `children` – Child requirements in the hierarchy.

- **`ComplianceControlTree`**  
  Maintains the root node and uses requirement ID segment depth to
  build the hierarchy (e.g., `1` → `1.1` → `1.1.1`).

- **`YamlFormatter`**  
  Walks the tree and renders YAML output including a standard PCI DSS
  header and properly indented titles.

- **PDF Processing Helpers**  
  Functions such as `extract_spec_tables`, `find_requirements_column_index`,
  and `extract_requirement_blobs` isolate PDF- and table-specific logic.

## Data Flow

1. **PDF Load** – `pdfplumber.open()` loads the PCI DSS PDF.
2. **Table Extraction** – `extract_spec_tables()` collects tables from all pages.
3. **Column Detection** – `find_requirements_column_index()` finds the
   "Requirements and Testing Procedures" column.
4. **Blob Concatenation** – `extract_requirement_blobs()` merges table cells
   into requirement text blobs keyed by requirement ID.
5. **Tree Build** – `ComplianceControlTree.add_node_from_blob()` parses
   IDs and titles and attaches nodes based on depth.
6. **Output** – `YamlFormatter` or JSON serialization produce structured
   output for downstream tooling.

## Security & Compliance Considerations

- The parser handles **public standard PDFs only** and should never be
  fed sensitive customer or transaction data.
- All outputs are **draft artifacts** and must be reviewed and validated
  by human assessors.
- See `docs/SECURITY_STANDARDS.md` for secure development and usage guidance.
