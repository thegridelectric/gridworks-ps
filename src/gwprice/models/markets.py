from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from gwprice.models.p_nodes import Base


class MarketSql(Base):
    __tablename__ = "markets"
    name = Column(String, primary_key=True)
    market_type_name = Column(String, nullable=False)
    p_node_alias = Column(String, ForeignKey("p_nodes.alias"), nullable=False)
    category = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    p_node = relationship("PNodeSql", back_populates="markets")
    hourly_channels = relationship(
        "HourlyPriceForecastChannelSql", back_populates="market"
    )

    def to_dict(self):
        return {
            "Name": self.name,
            "MarketTypeName": self.market_type_name,
            "PNodeAlias": self.p_node_alias,
            "Category": self.category,
            "Unit": self.unit,
        }
