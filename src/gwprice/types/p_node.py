from typing import Optional, Literal

from gwprice.property_format import LeftRightDot, UUID4Str
from gwprice.types import GwBase


class PNode(GwBase):
    id: UUID4Str
    alias: LeftRightDot
    prev_alias: Optional[LeftRightDot] = None
    display_name: Optional[str] = None
    iso_location_info: Optional[str] = None
    type_name: Literal["p.node"] = "p.node"
    version: Literal["000"] = "000"
