from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, tuple_
from sqlalchemy.orm import Session, relationship

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
    method = relationship("ForecastMethodSql", back_populates="hourly_channels")
    forecasts = relationship("HourlyPriceForecastSql", back_populates="channel")

    def to_dict(self):
        return {
            "Name": self.name,
            "MarketName": self.market_name,
            "TotalHours": self.total_hours,
            "MethodAlias": self.method_alias,
        }


def bulk_insert_channels(
    session: Session, channels: List[HourlyPriceForecastChannelSql]
):
    if not all(isinstance(obj, HourlyPriceForecastChannelSql) for obj in channels):
        raise ValueError("All objects must be HourlyPriceForecastChannelSql objects")

    batch_size = 100
    unique_columns = [
        HourlyPriceForecastChannelSql.market_name,
        HourlyPriceForecastChannelSql.total_hours,
        HourlyPriceForecastChannelSql.method_alias,
    ]

    for i in range(0, len(channels), batch_size):
        try:
            batch = channels[i : i + batch_size]

            # Gather primary key and unique constraints for batch
            pk_set = {channel.name for channel in batch}
            unique_set = {
                tuple(getattr(channel, col.name) for col in unique_columns)
                for channel in batch
            }

            # Query existing primary keys in the batch
            existing_pks = {
                result[0]
                for result in session.query(HourlyPriceForecastChannelSql.name)
                .filter(HourlyPriceForecastChannelSql.name.in_(pk_set))
                .all()
            }

            # Query existing unique combinations in the batch
            existing_uniques = set(
                session.query(*unique_columns)
                .filter(tuple_(*unique_columns).in_(unique_set))
                .all()
            )

            # Filter new channels based on both pk and unique constraints
            new_channels = [
                channel
                for channel in batch
                if channel.name not in existing_pks
                and tuple(getattr(channel, col.name) for col in unique_columns)
                not in existing_uniques
            ]

            print(
                f"Inserting {len(new_channels)} forecast channels out of {len(batch)}"
            )

            if new_channels:
                session.bulk_save_objects(new_channels)
                session.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
