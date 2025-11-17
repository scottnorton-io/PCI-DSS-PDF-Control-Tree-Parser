#!/usr/bin/env python3
"""
notion_export.py

Convert JSON output from the PCI DSS PDF Control Tree Parser into a
Notion-import-ready nested structure.

Usage:
    python examples/notion_export.py controls.json notion_import.json

The resulting JSON can be imported into Notion via:
- /import → JSON
- Or via the Notion API with a create-blocks loop

All outputs are draft artifacts requiring human review.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_tree(json_path: str) -> List[Dict[str, Any]]:
    """Load the parser's JSON tree structure."""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        sys.exit(f"Error loading JSON: {e}")


def notion_page(title: str, children: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Build a Notion page-like block structure.
    Used for Notion bulk JSON import.
    """
    page = {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "rich_text": [{"type": "text", "text": {"content": title}}],
        },
    }

    if children:
        page["children"] = children

    return page


def notion_block_text(text: str) -> Dict[str, Any]:
    """Simple text block for Notion."""
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
        },
    }


def convert_node(node: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a single requirement node into a Notion block (page)
    with nested children.
    """
    title = f"{node['id']} — {node['title']}"
    children = []

    # Add explanatory block
    children.append(
        notion_block_text("This requirement was parsed from the official PCI DSS v4.0.1 PDF.")
    )

    # Recursive children
    for child in node.get("children", []):
        children.append(convert_node(child))

    return notion_page(title, children)


def convert_tree_to_notion(tree: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert the entire parsed tree to Notion block format."""
    notion_blocks = []

    for node in tree:
        notion_blocks.append(convert_node(node))

    return notion_blocks


def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python examples/notion_export.py controls.json notion_import.json")

    input_json = sys.argv[1]
    output_json = sys.argv[2]

    tree = load_tree(input_json)
    notion_output = convert_tree_to_notion(tree)

    try:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(notion_output, f, indent=2, ensure_ascii=False)
        print(f"Notion import JSON written to {output_json}")
    except Exception as e:
        sys.exit(f"Error writing Notion JSON: {e}")


if __name__ == "__main__":
    main()
