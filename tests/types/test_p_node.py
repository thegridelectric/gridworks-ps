"""Tests p.node type, version 000"""

from gwprice.types import PNode


def test_p_node_generated() -> None:
    d = {
        "Id": "7286b617-bd15-4b26-8993-96285827432b",
        "Alias": "hw1.isone.ver.keene",
        "IsoId": "43790",
        "IsoLocationInfo": "LD.KEENE_RD46, NETWORK NODE",
        "DisplayName": "Keene Rd PNode",
        "TypeName": "p.node",
        "Version": "000",
    }

    assert PNode.from_dict(d).to_dict() == d
