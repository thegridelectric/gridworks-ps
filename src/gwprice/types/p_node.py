"""Type p.node, version 000"""

from typing import Literal, Optional

from gwprice.property_format import (
    LeftRightDot,
    UUID4Str,
)
from gwprice.types.gw_base import GwBase


class PNode(GwBase):
    id: UUID4Str
    alias: LeftRightDot
    iso_id: Optional[str] = None
    iso_location_info: Optional[str] = None
    prev_alias: Optional[LeftRightDot] = None
    display_name: Optional[str] = None
    type_name: Literal["p.node"] = "p.node"
    version: Literal["000"] = "000"
