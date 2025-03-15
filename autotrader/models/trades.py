from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from autotrader.db.database import Base

class Trade(Base):
    __tablename__ = "trades_log"

    id = Column(Integer, primary_key=True)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    side = Column(String)
    status = Column(String)
    result = Column(String)
    roi = Column(Float)