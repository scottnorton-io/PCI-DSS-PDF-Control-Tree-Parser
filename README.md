# PCI DSS v4.0.1 PDF Control Tree Parser

This repository contains a Python tool that parses the PCI DSS v4.0.1 PDF
and produces a hierarchical control tree in YAML or JSON format suitable
for further automation and mapping.

> **AI Use Disclosure**  
> AI-assisted tools may be used to help draft code and documentation.  
> These tools never make compliance determinations.  
> All outputs are reviewed and validated by a qualified assessor.

## Quick Start

```bash
# clone repo
git clone https://github.com/scottnorton-io/PCI-DSS-PDF-Control-Tree-Parser.git
cd PCI-DSS-PDF-Control-Tree-Parser

# create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# run the parser (YAML output)
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /path/to/PCI-DSS-v4_0_1.pdf \
  -f yaml \
  -o controls.yaml
```

Or use the helper script:

```bash
./scripts/run_parser.sh /path/to/PCI-DSS-v4_0_1.pdf yaml controls.yaml
```

## Status & Metadata

```plaintext
status: "Draft – AI Generated"
reviewer: "TBD"
validation_date: "TBD"
source_reference: "PCI-DSS-v4.0.1-PDF-Parser"
```

All parser outputs are **draft artifacts** and MUST be reviewed and
validated by a qualified PCI DSS assessor before being used in any
formal ROC or AOC.
