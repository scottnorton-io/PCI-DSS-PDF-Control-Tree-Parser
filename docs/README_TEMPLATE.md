# PCI DSS v4.0.1 PDF Control Tree Parser

Short project description here.

## Features

- Parses PCI DSS v4.0.1 PDF.
- Extracts "Requirements and Testing Procedures" column.
- Builds a hierarchical control tree (1 → 1.1 → 1.1.1, A1 → A1.1, etc.).
- Outputs YAML or JSON for downstream automation.

## Usage

```bash
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /path/to/PCI-DSS-v4_0_1.pdf \
  -f yaml \
  -o controls.yaml
```

## AI Use Disclosure

We use AI-assisted tools to help draft code and documentation.
These tools never make compliance determinations.
All outputs are reviewed and validated by a qualified assessor.
