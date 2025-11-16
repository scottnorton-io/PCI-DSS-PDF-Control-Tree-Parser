# PCI DSS v4.0.1 Requirements Parser

This tool parses the PCI DSS v4.0.1 PDF and produces a hierarchical control tree
in YAML or JSON format suitable for further automation and mapping.

## Usage

```bash
python3 pci_dss_parser.py /path/to/PCI-DSS-v4_0_1.pdf -f yaml -o controls.yaml
python3 pci_dss_parser.py /path/to/PCI-DSS-v4_0_1.pdf -f json -o controls.json
