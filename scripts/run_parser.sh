#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 /path/to/PCI-DSS-v4_0_1.pdf [yaml|json] [output_file]"
  exit 1
fi

PDF_PATH="$1"
FORMAT="${2:-yaml}"
OUTPUT="${3:-controls.${FORMAT}}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f "${PROJECT_ROOT}/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "${PROJECT_ROOT}/.venv/bin/activate"
fi

python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  "$PDF_PATH" \
  -f "$FORMAT" \
  -o "$OUTPUT"

echo "Output written to $OUTPUT"
