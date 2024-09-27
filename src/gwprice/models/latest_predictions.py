from sqlalchemy import Column, Integer, String

from gwprice.models.p_nodes import Base


class LatestPredictionSql(Base):
    __tablename__ = "latest_predictions"
    market_slot_name = Column(String, primary_key=True)
    value = Column(Integer, nullable=False)
    last_updated_s = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "Name": self.market_slot_name,
            "Value": self.value,
            "LastUpdatedS": self.last_updated_s,
        }
