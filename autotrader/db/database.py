from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

Base = declarative_base()
# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Database:
    def __init__(self):
        self.engine = engine
        self.create_tables()  # Ensure tables are created

    def create_tables(self):
        """Create tables based on ORM models"""
        import autotrader.models.symbol
        Base.metadata.create_all(self.engine)

# Create an instance of Database
db = Database()
