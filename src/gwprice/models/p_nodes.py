from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship

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

    markets = relationship("MarketSql", back_populates="p_node")

    def to_dict(self):
        d = {
            "Id": self.id,
            "Alias": self.alias,
        }
        if self.prev_alias:
            d["PrevAlias"] = self.prev_alias

        if self.display_name:
            d["DisplayName"] = self.display_name
        return d
