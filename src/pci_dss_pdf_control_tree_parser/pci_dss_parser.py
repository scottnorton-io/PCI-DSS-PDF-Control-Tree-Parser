#!/usr/bin/env python3
"""
PCI DSS v4.0.1 Requirements Parser

Parses PCI DSS v4.0.1 PDF tables and emits a hierarchical control tree
in YAML (default) or JSON format.

- Extracts from the "Requirements and Testing Procedures" column.
- Derives requirement IDs like 1, 1.1, 1.1.1, A1.1.1, etc.
- Builds a tree using ID segment depth (1 → 1.1 → 1.1.1).
- Outputs YAML with a standard PCI DSS header or structured JSON.

Usage:
    python3 pci_dss_parser.py path/to/PCI-DSS-v4_0_1.pdf -f yaml -o controls.yaml
"""

import argparse
import itertools
import json
import os
import re
import sys
import textwrap
from typing import Any, List, Optional

import pdfplumber

# ---------------------------------------------------------------------------
# Constants & Patterns
# ---------------------------------------------------------------------------

# Requirement index pattern:
# - Optional leading letter (A for A1.., A2..)
# - One or more numeric segments separated by dots (1, 1.1, 1.1.1, 2.3.4, etc.)
REQ_INDEX_REGEX = r'^[A-Z]?\d+(?:\.\d+)*\s'
REQ_INDEX_PATTERN = re.compile(REQ_INDEX_REGEX)

# Normalized header value for the column we care about
HEADER_COL_NORMALIZED = "requirements and testing procedures"

# Header template at top of YAML output
HEADER_TEMPLATE = """policy: PCI-DSS
title: Configuration Recommendations of a GNU/Linux System
id: pcidss_4
version: '4'
source: https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf
levels:
  - id: base
controls:
"""


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

class ComplianceControlNode:
    """
    Represents one PCI DSS requirement node in the control tree.
    """

    # Patterns used to separate title text from trailing notes/clauses.
    # The patterns capture the title in group 1 and discard the rest.
    title_split_patterns = [
        r'(?s)(.*)including,? but not limited to failure of:\s*\n',
        r'(?s)(.*)including,? but not limited to:\s*\n',
        r'(?s)(.*),?\s*including mechanisms that are:\s*\n',
        r'(?s)(.*),?\s*that meets the following:\s*\n',
        r'(?s)(.*),?\s*code changes are:\s*\n',
        r'(?s)(.*),?\s*that includes:\s*\n',
        r'(?s)(.*),?\s*and includes:\s*\n',
        r'(?s)(.*),?\s*and include:\s*\n',
        r'(?s)(.*),?\s*as follows:\s*\n',
        r'(?s)(.*),?\s*including:\s*\n',
        r'(?s)(.*),?\s*such that:\s*\n',
        r'(?s)(.*),?\s*are:\s*\n',
        r'(?s)(.*),?\s*is:\s*\n',
        r'(?s)(.*):\s*\n',
        r'(?s)(.*)PCI DSS Reference:\s*',
    ]

    def __init__(
        self,
        *,
        raw_blob: str,
        root: Optional["ComplianceControlNode"] = None
    ) -> None:
        self.raw_blob: str = raw_blob
        self.id: Optional[str] = None
        self.title: str = ""
        self.parent: Optional["ComplianceControlNode"] = None
        self.children: List["ComplianceControlNode"] = []
        self.depth: int = 0
        self.indent: str = "  "      # 2 spaces
        self.wrap_length: int = 98   # line wrap width for YAML title

        # Derive ID & title
        self._parse_id_and_title()

        # Root is only used to compute depth later by tree builder
        self._root = root

    @classmethod
    def from_blob(
        cls,
        blob: str,
        root: Optional["ComplianceControlNode"] = None
    ) -> "ComplianceControlNode":
        """
        Factory method to build a node from a requirement blob.
        """
        return cls(raw_blob=blob, root=root)

    def _parse_id_and_title(self) -> None:
        """
        Extract the requirement ID and cleaned title from the raw blob.
        """
        text = self.raw_blob.strip()
        if not text:
            return

        # ID from beginning of line using the compiled pattern
        m = REQ_INDEX_PATTERN.match(text)
        if m:
            self.id = m.group(0).strip()

        # Title candidate: original text minus obvious line breaks
        title_candidate = text

        # Apply splitting patterns to truncate at the first matching phrase
        for splitter in self.title_split_patterns:
            mt = re.search(splitter, title_candidate)
            if mt:
                title_candidate = mt.group(1)
                break

        # Normalize whitespace, replace trailing comma with period
        cleaned = title_candidate.replace("\n", " ").strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        cleaned = re.sub(r",$", ".", cleaned)
        self.title = cleaned

    def add_child(self, node: "ComplianceControlNode") -> None:
        self.children.append(node)
        node.parent = self

    def to_dict(self) -> dict:
        """
        Convert node (and its children) into a serializable dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "children": [child.to_dict() for child in self.children],
        }


class ComplianceControlTree:
    """
    Represents the entire control tree. Uses ID segment depth to build the
    hierarchy (1 → 1.1 → 1.1.1, A1 → A1.1, etc.).
    """

    def __init__(self) -> None:
        self.root = ComplianceControlNode(raw_blob="", root=None)
        self.root.id = None
        self.root.title = "ROOT"
        self.root.depth = 0
        self.last_by_depth: dict[int, ComplianceControlNode] = {0: self.root}

    def add_node_from_blob(self, blob: str) -> None:
        """
        Create a node from the given blob and attach it to the tree based on ID depth.
        """
        node = ComplianceControlNode.from_blob(blob, root=self.root)

        if not node.id:
            # Skip if we couldn't parse a requirement ID
            return

        depth = len(node.id.split("."))

        # Parent is the last node seen at depth-1, or root if not found
        parent = self.last_by_depth.get(depth - 1, self.root)
        parent.add_child(node)
        node.depth = parent.depth + 1

        # Track this as the last node at this depth
        self.last_by_depth[depth] = node

    def to_dict(self) -> List[dict]:
        """
        Represent the tree as a list of children (root-level requirements).
        """
        return [child.to_dict() for child in self.root.children]


# ---------------------------------------------------------------------------
# Formatting for output (YAML / JSON)
# ---------------------------------------------------------------------------

class YamlFormatter:
    """
    Renders the ComplianceControlTree as YAML, including the header template.
    """

    def __init__(
        self,
        root: ComplianceControlNode,
        wrap_length: int = 98,
        indent: str = "  ",
    ) -> None:
        self.root = root
        self.wrap_length = wrap_length
        self.indent = indent

    def format(self) -> str:
        """
        Return full YAML text as a single string.
        """
        lines: List[str] = [HEADER_TEMPLATE.rstrip()]
        for child in self.root.children:
            self._walk(child, lines)
        return "\n".join(lines)

    def _walk(self, node: ComplianceControlNode, lines: List[str]) -> None:
        """
        Depth-first traversal to append lines for each node.
        """
        lines.extend(self._format_node(node))
        for child in node.children:
            self._walk(child, lines)

    def _wrap_title(self, title: str, depth: int) -> str:
        """
        Wrap title text with proper indentation and width.
        """
        if not title:
            return ""

        # Base indentation for the node line (e.g., "  - id: ...")
        node_indent = self.indent * depth
        # Title is printed on: "  title: '...'"
        title_prefix = f"{node_indent}  title: "
        width = self.wrap_length - len(title_prefix)

        wrapped = textwrap.fill(
            title,
            width=width,
            initial_indent="",
            subsequent_indent="",
        )
        return wrapped

    def _format_node(self, node: ComplianceControlNode) -> List[str]:
        indent = self.indent * node.depth
        wrapped_title = self._wrap_title(node.title, node.depth)

        lines: List[str] = [
            f"{indent}- id: Req-{node.id}",
            f"{indent}  title: '{wrapped_title}'",
            f"{indent}  levels:",
            f"{indent}    - base",
            f"{indent}  status: not applicable",
        ]
        if node.children:
            lines.append(f"{indent}  controls:")
        else:
            lines.append(f"{indent}  rules: []")
            lines.append("")  # blank line between leaf nodes
        return lines


# ---------------------------------------------------------------------------
# PDF & Table Processing
# ---------------------------------------------------------------------------

def extract_spec_tables(doc: pdfplumber.PDF) -> List[List[List[Any]]]:
    """
    Extract all tables from the PDF.
    Returns a list of tables, each table is a list of rows,
    each row is a list of cell values.
    """
    tables: List[List[List[Any]]] = []
    for page in doc.pages:
        page_tables = page.extract_tables()
        if page_tables:
            tables.extend(page_tables)
    return tables


def find_requirements_column_index(table: List[List[Any]]) -> Optional[int]:
    """
    Given a table, try to find the index of the 'Requirements and Testing Procedures' column.
    Returns the column index if found, otherwise None.
    """
    if not table:
        return None

    header_row = table[0]
    lowered = [str(c).strip().lower() for c in header_row]

    for idx, val in enumerate(lowered):
        # Support minor variations like "(cont.)" etc.
        if HEADER_COL_NORMALIZED in val:
            return idx
    return None


def should_ignore_cell_header(text: str) -> bool:
    """
    Return True if this cell contains column headers we want to skip
    (e.g., Customized Approach Objective, Applicability Notes, etc.).
    """
    ignore_pattern = re.compile(
        r'^(Customized Approach Objective|Applicability Notes|Defined Approach Requirements)\b',
        re.IGNORECASE,
    )
    return bool(ignore_pattern.match(text))


def update_list_req(
    list_req: List[str],
    req_index: int,
    cell: Any
) -> int:
    """
    Update the list of requirement blobs with a new table cell.
    - If the cell starts with a requirement ID, start a new blob.
    - Otherwise, append to the current blob (if any).
    """
    if cell is None:
        return req_index

    text = str(cell).strip()
    if not text:
        return req_index

    if should_ignore_cell_header(text):
        return req_index

    if REQ_INDEX_PATTERN.match(text):
        # Start a new requirement blob
        req_index += 1
        list_req.append(text)
    elif req_index >= 0:
        # Append to current requirement blob
        list_req[req_index] += " " + text

    return req_index


def extract_requirement_blobs(tables: List[List[List[Any]]]) -> List[str]:
    """
    From all tables, extract concatenated requirement blobs from the
    'Requirements and Testing Procedures' column.
    """
    list_req: List[str] = []
    req_index: int = -1

    for tbl in tables:
        col_index = find_requirements_column_index(tbl)
        if col_index is None:
            continue

        # Skip header row (index 0). Remaining rows contain data.
        for row in tbl[1:]:
            cell = row[col_index] if col_index < len(row) else ""
            req_index = update_list_req(list_req, req_index, cell)

    return list_req


# ---------------------------------------------------------------------------
# CLI & Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract PCI DSS requirements from PDF into a hierarchical control tree."
    )
    parser.add_argument(
        "pdf",
        help="Path to PCI DSS PDF file (e.g., PCI-DSS-v4_0_1.pdf)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Output format (default: yaml)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path (if omitted, prints to stdout)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pdf_path = os.path.realpath(args.pdf)
    if not os.path.exists(pdf_path):
        sys.exit(f"Error: PDF not found at path: {pdf_path}")

    try:
        with pdfplumber.open(pdf_path) as pdfdoc:
            tables = extract_spec_tables(pdfdoc)
    except Exception as e:
        sys.exit(f"Error opening PDF: {e}")

    if not tables:
        sys.exit("No tables found in the PDF. Cannot proceed.")

    blobs = extract_requirement_blobs(tables)
    if not blobs:
        sys.exit("No requirement blobs extracted. Check PDF structure and table headers.")

    tree = ComplianceControlTree()
    for blob in blobs:
        tree.add_node_from_blob(blob)

    if args.format == "yaml":
        formatter = YamlFormatter(tree.root)
        output_text = formatter.format()
    else:
        output_text = json.dumps(tree.to_dict(), indent=2, ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_text)
        except OSError as e:
            sys.exit(f"Error writing to output file: {e}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
