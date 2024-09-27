from typing import List

from sqlalchemy import Column, String
from sqlalchemy.exc import NoSuchTableError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import Session, relationship

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


def bulk_insert_forecast_methods(
    session: Session, forecast_methods: List[ForecastMethodSql]
):
    if not all(isinstance(obj, ForecastMethodSql) for obj in forecast_methods):
        raise ValueError(
            "All objects in forecast_methods must be ForecastMethodSql objects"
        )

    batch_size = 10

    for i in range(0, len(forecast_methods), batch_size):
        try:
            batch = forecast_methods[i : i + batch_size]
            pk_column = ForecastMethodSql.alias
            pk_set = set()

            for forecast in batch:
                pk_set.add(forecast.alias)

            existing_pks = set(
                session.query(pk_column).filter(pk_column.in_(pk_set)).all()
            )

            new_forecasts = [
                forecast for forecast in batch if forecast.alias not in existing_pks
            ]
            print(f"Inserting {len(new_forecasts)} out of {len(batch)}")

            session.bulk_save_objects(new_forecasts)
            session.commit()

        except NoSuchTableError as e:
            print(f"Error: The table does not exist. {e}")
            session.rollback()
        except OperationalError as e:
            print(f"Operational Error! {e}")
            session.rollback()
        except SQLAlchemyError as e:
            print(f"An error occurred: {e}")
            session.rollback()
