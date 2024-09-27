from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint

from gwprice.models.p_nodes import Base


class PriceSql(Base):
    __tablename__ = "prices"
    market_slot_name = Column(String, primary_key=True)
    market_name = Column(String, ForeignKey("markets.name"), nullable=False)
    slot_start_s = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "market_name",
            "slot_start_s",
            name="uq_from_market_and_start",
        ),
    )

    def to_dict(self):
        return {
            "MarketSlotName": self.market_slot_name,
            "MarketName": self.market_name,
            "SlotStartS": self.slot_start_s,
            "Price": self.price,
        }
