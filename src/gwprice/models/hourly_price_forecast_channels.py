"""
Hourly Price Forecast Channels
"""

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from gwprice.models.p_nodes import Base


class HourlyPriceForecastChannelSql(Base):
    __tablename__ = "hpf_channels"
    name = Column(String, primary_key=True)
    market_name = Column(String, ForeignKey("markets.name"), nullable=False)
    total_hours = Column(Integer, nullable=False)
    method_alias = Column(String, ForeignKey("forecast_methods.alias"), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "market_name",
            "total_hours",
            "method_alias",
            name="uq_from_market, hrs, method",
        ),
    )

    market = relationship("MarketSql", back_populates="hourly_channels")
    method = relationship("PriceMethodSql", back_populates="hourly_channels")
    forecasts = relationship("HourlyPriceForecastSql", back_populates="channel")

    def to_dict(self):
        return {
            "Name": self.name,
            "PNodeAlias": self.market_name,
            "TotalHours": self.total_hours,
            "MethodAlias": self.method_alias,
        }
