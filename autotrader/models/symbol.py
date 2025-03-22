from sqlalchemy import Column, Integer, Float, DateTime
from autotrader.db.database import Base

class Symbol(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
