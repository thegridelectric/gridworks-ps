from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import Session, declarative_base, relationship

# Define the base class
# NOTE: for any other model do this:
# from gwprice.models.p_nodes import Base
Base = declarative_base()


class PNodeSql(Base):
    __tablename__ = "p_nodes"
    id = Column(String, primary_key=True)
    alias = Column(String, nullable=False, unique=True)
    prev_alias = Column(String)
    display_name = Column(String)
    iso_id = Column(String)
    iso_location_info = Column(String)
    markets = relationship("MarketSql", back_populates="p_node")

    def __repr__(self):
        return self.alias

    def __str__(self):
        return self.alias

    def to_dict(self):
        d = {
            "Id": self.id,
            "Alias": self.alias,
        }
        if self.prev_alias:
            d["PrevAlias"] = self.prev_alias

        if self.display_name:
            d["DisplayName"] = self.display_name

        if self.iso_location_info:
            d["IsoLocationInfo"] = self.iso_location_info
        return d


def bulk_insert_p_nodes(session: Session, p_nodes: List[PNodeSql]):
    if not all(isinstance(obj, PNodeSql) for obj in p_nodes):
        raise ValueError("All objects in p_nodes must be PNodeSql objects")

    batch_size = 100

    for i in range(0, len(p_nodes), batch_size):
        try:
            batch = p_nodes[i : i + batch_size]
            pk_set = set()
            alias_set = set()

            for p_node in batch:
                pk_set.add(p_node.id)
                alias_set.add(p_node.alias)

            existing_pks = {
                result[0]
                for result in session.query(PNodeSql.id)
                .filter(PNodeSql.id.in_(pk_set))
                .all()
            }

            existing_aliases = {
                result[0]
                for result in session.query(PNodeSql.alias)
                .filter(PNodeSql.alias.in_(alias_set))
                .all()
            }

            new_p_nodes = [
                p_node
                for p_node in batch
                if p_node.id not in existing_pks
                and p_node.alias not in existing_aliases
            ]
            print(f"Inserting {len(new_p_nodes)} p_nodes out of {len(batch)}")

            if new_p_nodes:
                session.bulk_save_objects(new_p_nodes)
                session.commit()

        except Exception as e:
            print(f"Error occurred: {e}")
            session.rollback()
