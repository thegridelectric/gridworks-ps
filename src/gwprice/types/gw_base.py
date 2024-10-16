import json
from typing import Any, Dict, Literal, Type, TypeVar

from gw.errors import GwTypeError
from gw.utils import recursively_pascal, snake_to_pascal
from pydantic import BaseModel, ConfigDict, ValidationError

T = TypeVar("T", bound="GwBase")


class GwBase(BaseModel):
    type_name: Literal["gw.base"] = "gw.base"
    version: Literal["000"] = "000"

    model_config = ConfigDict(
        alias_generator=snake_to_pascal,
        frozen=True,
        populate_by_name=True,
        use_enum_values=True,
    )

    @classmethod
    def from_dict(cls: Type[T], d: dict) -> T:
        if not recursively_pascal(d):
            raise GwTypeError(f"dict is not recursively pascal case! {d}")
        try:
            t = cls(**d)
        except ValidationError as e:
            raise GwTypeError(f"Pydantic validation error: {e}") from e
        return t

    def to_dict(self) -> Dict[str, Any]:
        d = self.model_dump(exclude_none=True, by_alias=True)
        return d

    def to_type(self) -> bytes:
        """
        Serialize to the get.hourly.price.forecast.channel.000 representation designed to send in a message.
        """
        json_string = json.dumps(self.to_dict())
        return json_string.encode("utf-8")

    @classmethod
    def type_name_value(cls) -> str:
        # Automatically return the type_name defined in the subclass
        return cls.model_fields["type_name"].default
