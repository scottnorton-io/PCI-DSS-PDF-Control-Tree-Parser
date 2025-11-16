import json

from pci_dss_pdf_control_tree_parser.pci_dss_parser import (
    ComplianceControlTree,
    extract_requirement_blobs,
    find_requirements_column_index,
)


def test_find_requirements_column_index():
    table = [
        ["Other Column", "Requirements and Testing Procedures", "Foo"],
        ["x", "1 Establish and implement firewall configuration.", "y"],
    ]
    idx = find_requirements_column_index(table)
    assert idx == 1


def test_extract_requirement_blobs_simple():
    tables = [
        [
            ["Col1", "Requirements and Testing Procedures"],
            ["x", "1 Install and maintain network security controls."],
            ["y", "1.1 Documented firewall standards are maintained."],
        ]
    ]
    blobs = extract_requirement_blobs(tables)
    assert len(blobs) == 2
    assert blobs[0].startswith("1 ")
    assert blobs[1].startswith("1.1 ")


def test_tree_build_from_blobs():
    tree = ComplianceControlTree()
    blobs = [
        "1 Install and maintain network security controls.",
        "1.1 A sub-requirement of 1.",
        "1.1.1 A child of 1.1.",
    ]
    for b in blobs:
        tree.add_node_from_blob(b)

    root_children = tree.to_dict()
    assert len(root_children) == 1
    r1 = root_children[0]
    assert r1["id"] == "1"
    assert len(r1["children"]) == 1
    r11 = r1["children"][0]
    assert r11["id"] == "1.1"
    assert len(r11["children"]) == 1
    assert r11["children"][0]["id"] == "1.1.1"
