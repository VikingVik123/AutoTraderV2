import pytest
from unittest.mock import MagicMock
from datetime import datetime
from autotrader.models.symbol import Symbol

@pytest.fixture
def mock_db_session():
    """Creates a mock SQLAlchemy session."""
    return MagicMock()

def test_symbol_creation(mock_db_session):
    """Test inserting a Symbol record using a mock database session."""
    symbol = Symbol(datetime=datetime.utcnow(), open=45000.0, high=46000.0, low=44000.0, close=45500.0, volume=1000)

    mock_db_session.add(symbol)
    mock_db_session.commit()

    mock_db_session.add.assert_called_once_with(symbol)
    mock_db_session.commit.assert_called_once()

def test_symbol_query(mock_db_session):
    """Test querying a Symbol record using a mock session."""
    fake_symbol = Symbol(id=1, datetime=datetime.utcnow(), open=45000.0, high=46000.0, low=44000.0, close=45500.0, volume=1000)

    mock_db_session.query().filter_by().first.return_value = fake_symbol

    
