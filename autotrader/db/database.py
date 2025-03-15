from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Database:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"), echo=False)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        Base.metadata.create_all(self.engine)

    def create_tables(self):
        """
        Create tables based on ORM models
        """
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Return the session object
        """
        return self.session
    
db = Database()