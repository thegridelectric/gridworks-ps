from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship

# Define the base class
# NOTE: for any other model do this:
# from gwprice.models.p_nodes import Base
Base = declarative_base()


class HourlyPriceForecastSql(Base):
    __tablename__ = "hourly_forecasts"
    price_uid = Column(String, primary_key=True)
    from_g_node_alias = Column(String, nullable=False)
    channel_name = Column(String, ForeignKey("hpf_channels.name"), nullable=False)
    start_unix_s = Column(Integer, nullable=False)
    hour_starting_prices = Column(JSONB, nullable=False)
    forecast_created_s = Column(Integer, nullable=False)

    channel = relationship("HourlyPriceForecastChannelSql", back_populates="forecasts")

    def to_dict(self):
        return {
            "PriceUid": self.price_uid,
            "FromGNodeALias": self.from_g_node_alias,
            "ChannelName": self.channel_name,
            "StartUnixS": self.start_unix_s,
            "HourStartingPrices": self.hour_starting_prices,
            "ForecastCreatedS": self.forecast_created_s,
        }
