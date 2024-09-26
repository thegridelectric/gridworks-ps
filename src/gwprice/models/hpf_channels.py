"""
Hourly Price Forecast Channels
"""

from sqlalchemy import  Integer, Column, String, UniqueConstraint
from sqlalchemy.orm import declarative_base

# Define the base class
Base = declarative_base()



class HpfChannelSql(Base):
    __tablename__ = "hpf_channels"
    name = Column(String, primary_key=True)
    p_node_alias = Column(String, nullable=False)
    category = Column(String, nullable=False)
    total_hours = Column(Integer, nullable=False)
    method_alias = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "p_node_alias",
            "category",
            "total_hours",
            "method_alias",
            name="uq_from_p_node_etc",
        ),
    )

    def to_dict(self):
        return {
            "Name": self.name,
            "PNodeAlias": self.p_node_alias,
            "Category": self.category,
            "TotalHours": self.total_hours,
            "MethodAlias": self.method_alias,
            "Unit": self.unit
        }
