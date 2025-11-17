Nice, let’s keep the train moving. I’ll add the next logical layer without touching your core parser: reusable exporters + docs.


Below are drop-in components:




docs/EXPORTERS.md – how to use/export to Notion + Vanta-style control set




examples/vanta_control_set_export.py – JSON → Vanta-style control set

(works on current parser JSON output)




You can paste these directly into the repo.



1️⃣ docs/EXPORTERS.md


Create docs/EXPORTERS.md:


# Exporters – Using the PCI DSS Control Tree in Other Tools

The parser’s main job is to convert the **PCI DSS v4.0.1 PDF** into a structured
hierarchical control tree (JSON/YAML). This document explains how to take that
JSON and feed it into downstream tools.

Current exporters:

- **Notion** – Simple hierarchical import (example script).
- **Vanta-style Control Set** – JSON matching Vanta’s control set style schema.

All exporters follow the same basic pattern:

1. Run the parser to generate **JSON**.
2. Run an exporter script under `examples/`.
3. Import the exporter’s JSON into your target platform or pipeline.

---

## 1. Generate the Base JSON Tree

From the project root, with your virtual environment active:

```bash
python -m pci_dss_pdf_control_tree_parser.pci_dss_parser \
  /absolute/path/to/PCI-DSS-v4_0_1.pdf \
  -f json \
  -o controls.json



This controls.json file is the canonical tree used by all exporters.



2. Notion Export (Recap)


Example script: examples/notion_export.py


Usage:


python examples/notion_export.py controls.json notion_import.json



Then in Notion:




Go to Import → JSON.




Upload notion_import.json.




You’ll get a nested structure where:




Each requirement (1, 1.1, 1.1.1, A1.1.1, etc.) becomes a heading block.




Titles include both ID and short description.






This is ideal for:




Browsing the standard inside Notion.




Annotating requirements, adding your own notes, and linking to other pages.






⚠️ Reminder: this is a convenience view of the PCI DSS standard, not a replacement

for reading the official documentation.





3. Vanta-Style Control Set Export


The Vanta control set schema represents a standard as:




A top-level “standard” object,




A list of “principles” (top-level sections),




Each with nested “controls”.




We provide a starter exporter that:




Maps each top-level requirement (e.g., 1, 2, …, A1, A2) to a principle.




Maps all children (1.1, 1.1.1, etc.) to controls under that principle.




Preserves IDs and titles from the parser output.




3.1 Usage


python examples/vanta_control_set_export.py controls.json vanta_control_set.json



This generates vanta_control_set.json with the following shape (simplified):


{
  "NOTICE": "Draft – AI Generated control set. Requires human review.",
  "standard": {
    "name": "PCI DSS v4.0.1",
    "principles": [
      {
        "id": "1",
        "name": "Install and maintain network security controls.",
        "controls": [
          {
            "id": "1.1",
            "title": "Network security controls are documented and implemented...",
            "description": "",
            "mappings": []
          }
        ]
      }
    ]
  }
}



This file can then be:




Used as a starting point for a Vanta-compatible control set.




Adapted into a GRC control mapping library.




Used as an internal standard index for your own tools.






📝 Important:

This exporter provides a structural mapping only. You will likely want to:




Adjust principle naming.




Enrich controls with descriptions, mappings, and metadata.




Validate the JSON against the latest Vanta schema before production use.







4. Extending Exporters


You can create additional exporters by following this pattern:




Load controls.json.




Walk the tree and transform it:




Keep IDs and titles intact.




Decide where to flatten or preserve hierarchy.






Emit JSON or YAML that matches your target schema.




Examples you might add later:




Fieldguide: Map the tree into a control catalog or evidence request set.




CSV: Flatten into simple rows: id,title,parent_id,depth.




Custom internal schema: For your own Notion/Obsidian/knowledge graph pipelines.




If you add new exporters:




Put scripts in examples/.




Document them in this file.




Add tests for the transformation functions (even minimal ones).





5. Status & Metadata


All exported artifacts are draft and must be validated:


status: "Draft – AI Generated"
reviewer: "TBD"
validation_date: "TBD"
source_reference: "PCI-DSS-v4.0.1-PDF-Parser-Export"



This keeps the compliance story clean:

AI-assisted parsing and exporting; human-reviewed decisions and conclusions.



---

## 2️⃣ `examples/vanta_control_set_export.py`

Create `examples/vanta_control_set_export.py`:

```python
#!/usr/bin/env python3
"""
vanta_control_set_export.py

Convert JSON output from the PCI DSS PDF Control Tree Parser into a
Vanta-style control set JSON structure.

Usage:
    python examples/vanta_control_set_export.py controls.json vanta_control_set.json

Notes:
- This script produces a *structural starting point* for a Vanta control set.
- You should validate/enrich the result against Vanta's current schema and your
  own internal conventions before using it in production.

All outputs are draft artifacts requiring human review.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


TreeNode = Dict[str, Any]


def load_tree(json_path: str) -> List[TreeNode]:
    """Load the parser's JSON tree structure."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected top-level JSON array from parser.")
        return data
    except Exception as e:
        sys.exit(f"Error loading JSON tree: {e}")


def is_top_level_id(req_id: str) -> bool:
    """
    Determine whether the given requirement ID should be treated
    as a 'principle' in the Vanta control set.
    """
    # Examples:
    # "1", "2", ... "12", "A1", "A2"
    return "." not in req_id


def flatten_controls(node: TreeNode) -> List[TreeNode]:
    """
    Flatten a requirement subtree into a list of nodes to be treated as "controls".
    Includes the node itself and all descendants.

    Each returned item retains:
    - id
    - title
    """
    results: List[TreeNode] = []

    def _walk(n: TreeNode) -> None:
        results.append({"id": n["id"], "title": n["title"]})
        for child in n.get("children", []):
            _walk(child)

    _walk(node)
    return results


def build_vanta_control(control_node: TreeNode) -> Dict[str, Any]:
    """
    Build a basic control structure from a flattened requirement node.
    This is intentionally minimal so you can enrich it later.
    """
    return {
        "id": control_node["id"],
        "title": control_node["title"],
        "description": "",
        "mappings": [],
    }


def build_principle(node: TreeNode) -> Dict[str, Any]:
    """
    Build a Vanta-style "principle" object from a top-level requirement node.
    All descendants become "controls" under this principle.
    """
    flattened = []

    # Include the node itself as a control
    flattened.append({"id": node["id"], "title": node["title"]})

    # Include all descendants
    for child in node.get("children", []):
        flattened.extend(flatten_controls(child))

    controls = [build_vanta_control(c) for c in flattened]

    return {
        "id": node["id"],
        "name": node["title"],
        "controls": controls,
    }


def convert_tree_to_vanta(tree: List[TreeNode]) -> Dict[str, Any]:
    """
    Convert the entire tree into a Vanta-style control set structure.

    Output shape (simplified):

    {
      "NOTICE": "...",
      "standard": {
        "name": "PCI DSS v4.0.1",
        "principles": [
          {
            "id": "1",
            "name": "Install and maintain network security controls.",
            "controls": [...]
          }
        ]
      }
    }
    """
    principles: List[Dict[str, Any]] = []

    for node in tree:
        req_id = node.get("id", "")
        if not isinstance(req_id, str):
            continue
        if not is_top_level_id(req_id):
            # Only treat top-level IDs as principles
            continue

        principles.append(build_principle(node))

    vanta_obj: Dict[str, Any] = {
        "NOTICE": (
            "Draft – AI Generated control set based on PCI DSS v4.0.1. "
            "Requires human review and validation against Vanta's current schema."
        ),
        "standard": {
            "name": "PCI DSS v4.0.1",
            "principles": principles,
        },
    }
    return vanta_obj


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(
            "Usage: python examples/vanta_control_set_export.py controls.json vanta_control_set.json"
        )

    input_json = sys.argv[1]
    output_json = sys.argv[2]

    tree = load_tree(input_json)
    vanta_obj = convert_tree_to_vanta(tree)

    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(vanta_obj, f, indent=2, ensure_ascii=False)
        print(f"Vanta-style control set JSON written to {output_json}")
    except Exception as e:
        sys.exit(f"Error writing Vanta control set JSON: {e}")


if __name__ == "__main__":
    main()




3️⃣ How to Use the New Bits


From repo root:


# 1) Generate base JSON from the PDF
pci-dss-parse /absolute/path/to/PCI-DSS-v4_0_1.pdf -f json -o controls.json

# 2) Export to Vanta-style control set
python examples/vanta_control_set_export.py controls.json vanta_control_set.json



Then:




Use vanta_control_set.json as a starting point for:




A Vanta control set




A generic GRC control library




Your own “trusted evidence connector” experiments







If you’d like the next logical step, I can:




Add a CSV exporter (flat table),




Or a Fieldguide-ready control/evidence mapping stub exporter,

tied into your earlier plan for Fieldguide scoping and worksheets.


