import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from autotrader.db.database import Base

# Use an in-memory SQLite database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Creates a new database session for each test."""
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # Create tables before test
    Base.metadata.create_all(engine)

    session = TestingSessionLocal()
    yield session  # Provide session to test

    # Cleanup after test
    session.close()
    Base.metadata.drop_all(engine)
