python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install .

pci-dss-parse PCI-DSS-v4_0_1.pdf -f yaml -o controls.yaml

# Run tests
pytest tests/test_parser_basic.py

# Run parser
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /path/to/PCI-DSS-v4_0_1.pdf \
  -f yaml \
  -o controls.yaml
