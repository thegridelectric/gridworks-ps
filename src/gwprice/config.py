"""Settings for a GridWorks JournalKeeper, readable from environment and/or from env files."""

from gwbase.config.rabbit_settings import RabbitBrokerClient
from pydantic import ConfigDict, SecretStr
from pydantic_settings import BaseSettings

# from gjk.config import RabbitBrokerClient


DEFAULT_ENV_FILE = ".env"


class Settings(BaseSettings):
    rabbit: RabbitBrokerClient = RabbitBrokerClient()
    db_url: SecretStr = SecretStr(
        "postgresql://gwprice:PASSWD@journaldb.electricity.works/pricedb"
    )
    db_pass: SecretStr = SecretStr("Passwd")

    model_config = ConfigDict(
        env_prefix="gwprice_",
        env_nested_delimiter="__",
        extra="ignore",
    )
