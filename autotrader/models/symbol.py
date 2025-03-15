from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from autotrader.db.database import Base

class Symbol(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

