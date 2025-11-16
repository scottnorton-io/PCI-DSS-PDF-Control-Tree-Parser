# macOS Python Virtual Environment Cookbook

This guide describes a robust, repeatable Python setup on macOS for
the PCI DSS PDF Control Tree Parser.

## 1. Clone the Repository

```bash
cd ~/Projects
git clone https://github.com/scottnorton-io/PCI-DSS-PDF-Control-Tree-Parser.git
cd PCI-DSS-PDF-Control-Tree-Parser
```

## 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run the Parser

```bash
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /absolute/path/to/PCI-DSS-v4_0_1.pdf \
  -f yaml \
  -o controls.yaml
```

Or:

```bash
./scripts/run_parser.sh /absolute/path/to/PCI-DSS-v4_0_1.pdf yaml controls.yaml
```

## 4. Notes

- All outputs are **draft** and must be reviewed by a qualified assessor.
- For more details, see `README.md` and `docs/ARCHITECTURE.md`.
