from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from gwprice.models.p_nodes import Base


class ForecastMethodSql(Base):
    __tablename__ = "forecast_methods"
    alias = Column(String, primary_key=True)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)

    hourly_channels = relationship(
        "HourlyPriceForecastChannelSql", back_populates="method"
    )

    def to_dict(self):
        return {
            "Alias": self.alias,
            "Category": self.category,
            "Description": self.description,
        }
