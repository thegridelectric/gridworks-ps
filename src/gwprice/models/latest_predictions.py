from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from gwprice.models.p_nodes import Base


class LatestPredictionSql(Base):
    __tablename__ = "latest_predictions"
    market_slot_name = Column(String, primary_key=True)
    market_name = Column(String, ForeignKey("markets.name"), nullable=False)
    slot_start_s = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    last_updated_s = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "market_name",
            "slot_start_s",
            name="uq_prediction_from_market_and_start",
        ),
    )

    def to_dict(self):
        return {
            "MarketSlotName": self.market_slot_name,
            "MarketName": self.market_name,
            "SlotStartS": self.slot_start_s,
            "Value": self.value,
            "LastUpdatedS": self.last_updated_s,
        }
