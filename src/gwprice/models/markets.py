from typing import List

from sqlalchemy import Column, ForeignKey, String, UniqueConstraint, tuple_
from sqlalchemy.orm import Session, relationship

from gwprice.models.p_nodes import Base


class MarketSql(Base):
    __tablename__ = "markets"
    name = Column(String, primary_key=True)
    market_type_name = Column(String, nullable=False)
    p_node_alias = Column(String, ForeignKey("p_nodes.alias"), nullable=False)
    category = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "market_type_name",
            "p_node_alias",
            "category",
            name="market_uq_type_pn_cat",
        ),
    )

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


def bulk_insert_markets(session: Session, markets: List[MarketSql]):
    if not all(isinstance(obj, MarketSql) for obj in markets):
        raise ValueError("All objects must be MarketSql objects")

    batch_size = 100
    unique_columns = [
        MarketSql.market_type_name,
        MarketSql.p_node_alias,
        MarketSql.category,
    ]

    for i in range(0, len(markets), batch_size):
        try:
            batch = markets[i : i + batch_size]

            # Gather primary key and unique constraints for batch
            pk_set = {market.name for market in batch}
            unique_set = {
                tuple(getattr(market, col.name) for col in unique_columns)
                for market in batch
            }

            # Query existing primary keys in the batch
            existing_pks = {
                result[0]
                for result in session.query(MarketSql.name)
                .filter(MarketSql.id.in_(pk_set))
                .all()
            }

            # Query existing unique combinations in the batch
            existing_uniques = set(
                session.query(*unique_columns)
                .filter(tuple_(*unique_columns).in_(unique_set))
                .all()
            )

            # Filter new markets based on both pk and unique constraints
            new_markets = [
                market
                for market in batch
                if market.name not in existing_pks
                and tuple(getattr(market, col.name) for col in unique_columns)
                not in existing_uniques
            ]

            print(f"Inserting {len(new_markets)} out of {len(batch)}")

            if new_markets:
                session.bulk_save_objects(new_markets)
                session.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
