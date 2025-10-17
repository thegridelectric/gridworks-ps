from typing import Literal, Optional

from gwprice.asl.codec import AslType
from gwprice.asl.property_format import (
    LeftRightDot,
    UUID4Str,
)


class PNode(AslType):
    id: UUID4Str
    alias: LeftRightDot
    iso_id: Optional[str] = None
    iso_location_info: Optional[str] = None
    prev_alias: Optional[LeftRightDot] = None
    display_name: Optional[str] = None
    tz: str = "America/New_York"
    type_name: Literal["p.node"] = "p.node"
    version: Literal["000"] = "000"
