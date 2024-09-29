from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from gwprice.models.p_nodes import Base


class HourlyPriceForecastSql(Base):
    __tablename__ = "hourly_forecasts"
    price_uid = Column(String, primary_key=True)
    from_g_node_alias = Column(String, nullable=False)
    channel_name = Column(String, ForeignKey("hpf_channels.name"), nullable=False)
    start_unix_s = Column(Integer, nullable=False)
    hour_starting_prices = Column(JSONB, nullable=False)
    forecast_created_s = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "channel_name",
            "start_unix_s",
            "forecast_created_s",
            name="forecast_uq_channel_start_created",
        ),
    )

    channel = relationship("HourlyPriceForecastChannelSql", back_populates="forecasts")

    def to_dict(self):
        return {
            "PriceUid": self.price_uid,
            "FromGNodeAlias": self.from_g_node_alias,
            "ChannelName": self.channel_name,
            "StartUnixS": self.start_unix_s,
            "HourStartingPrices": self.hour_starting_prices,
            "ForecastCreatedS": self.forecast_created_s,
        }
