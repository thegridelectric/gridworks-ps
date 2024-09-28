from typing import List

from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Session

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


def bulk_insert_prices(session: Session, prices: List[PriceSql]):
    if not all(isinstance(obj, PriceSql) for obj in prices):
        raise ValueError("All objects in prices must be PriceSql objects")

    batch_size = 10

    for i in range(0, len(prices), batch_size):
        try:
            batch = prices[i : i + batch_size]
            pk_set = set()

            for price in batch:
                pk_set.add(price.market_slot_name)

            existing_pks = {
                result[0]
                for result in session.query(PriceSql.market_slot_name)
                .filter(PriceSql.market_slot_name.in_(pk_set))
                .all()
            }

            new_prices = [
                price for price in batch if price.market_slot_name not in existing_pks
            ]
            print(f"Inserting {len(new_prices)} price methods out of {len(batch)}")

            session.bulk_save_objects(new_prices)
            session.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
