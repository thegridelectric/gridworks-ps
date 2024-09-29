from typing import List

from gwprice.types.p_node import PNode

MyPNodeDicts = [
    {
        "TypeName": "p.node",
        "Version": "000",
        "Id": "7b664806-1c1b-48fc-986a-89212694bd6c",
        "Alias": "hw1.isone",
    },
    {
        "TypeName": "p.node",
        "Version": "000",
        "Id": "d454872a-7410-430f-b8dc-82f7d4ddf244",
        "Alias": "hw1.isone.4007",
        "IsoId": "4007",
        "IsoLocationInfo": ".Z.WCMASS, LOAD ZONE",
    },
    {
        "TypeName": "p.node",
        "Version": "000",
        "Id": "edc9a04e-2291-4641-993d-343532f2004c",
        "Alias": "hw1.isone.4001",
        "IsoId": "4001",
        "IsoLocationInfo": ".Z.MAINE, LOAD ZONE",
    },
    {
        "TypeName": "p.node",
        "Version": "000",
        "Id": "ede1a8a7-8ffe-496e-8ef5-2bd8d5fabd90",
        "Alias": "hw1.isone.ver.keene.stetson",
        "IsoId": "16612",
        "IsoLocationInfo": "UN.STETSON 34.5STE2, NETWORK NODE",
    },
    {
        "TypeName": "p.node",
        "Version": "000",
        "Id": "7286b617-bd15-4b26-8993-96285827432b",
        "Alias": "hw1.isone.ver.keene",
        "IsoId": "43790",
        "IsoLocationInfo": "LD.KEENE_RD46, NETWORK NODE",
    },
]
MyPNodes: List[PNode] = [PNode.from_dict(d) for d in MyPNodeDicts]
