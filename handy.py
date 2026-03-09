
from gwprice.database import SessionLocal

db = SessionLocal()
from gwprice.models import PriceSql
from sqlalchemy import func

db.query(
    func.max(PriceSql.slot_start_s)
).filter(
    PriceSql.market_name == 'e.rt60gate5.hw1.isone.ver.keene'
).scalar()
