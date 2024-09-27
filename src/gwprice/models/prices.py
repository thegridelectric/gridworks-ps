from sqlalchemy import Column, Float, String

from gwprice.models.p_nodes import Base


class PriceSql(Base):
    __tablename__ = "prices"
    market_slot_name = Column(String, primary_key=True)
    price = Column(Float, nullable=False)

    def to_dict(self):
        return {
            "MarketSlotName": self.market_slot_name,
            "Price": self.price,
        }
