import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.append("./scripts")
from data_pipeline import run_pipeline  # noqa

API_KEY = os.getenv("API_KEY")


@pytest.fixture
def mock_get_exchange_data():
    with patch("data_pipeline.get_exchange_data") as mock:
        mock.return_value = [
            {
                "id": "binance",
                "name": "Binance",
                "year_established": 2017,
                "country": "Cayman Islands",
                "description": "",
                "url": "https://www.binance.com/",
                "has_trading_incentive": False,
                "trust_score": 10,
                "trust_score_rank": 1,
                "trade_vol_24h_btc": 258073.91462007,
                "trade_vol_24h_btc_normalized": 131978.47853064,
                "trade_vol_24h_usd": 17172011173.77,
                "trade_vol_24h_usd_normalized": 8781731820.37,
                "age_of_exchange": 7,
                "ingested_at": "2024-06-17 22:33:10.435522",
            },
            {
                "id": "bybit_spot",
                "name": "Bybit",
                "year_established": 2018,
                "country": "British Virgin Islands",
                "description": "Bybit is a cryptocurrency exchange",
                "url": "https://www.bybit.com",
                "has_trading_incentive": False,
                "trust_score": 10,
                "trust_score_rank": 2,
                "trade_vol_24h_btc": 77934.63145612,
                "trade_vol_24h_btc_normalized": 61321.27839195,
                "trade_vol_24h_usd": 5185701794.61,
                "trade_vol_24h_usd_normalized": 4080263901.48,
                "age_of_exchange": 6,
                "ingested_at": "2024-06-17 22:33:10.435522",
            },
            {
                "id": "huobi",
                "name": "HTX",
                "year_established": 2013,
                "country": "Seychelles",
                "description": "",
                "url": "https://www.huobi.com",
                "has_trading_incentive": False,
                "trust_score": 10,
                "trust_score_rank": 4,
                "trade_vol_24h_btc": 38242.42902179,
                "trade_vol_24h_btc_normalized": 38242.42902179,
                "trade_vol_24h_usd": 2544617573.77,
                "trade_vol_24h_usd_normalized": 2544617573.77,
                "age_of_exchange": 11,
                "ingested_at": "2024-06-17 22:33:10.435522",
            },
            {
                "id": "gdax",
                "name": "Coinbase Exchange",
                "year_established": 2012,
                "country": "United States",
                "description": "",
                "url": "https://www.coinbase.com/",
                "has_trading_incentive": False,
                "trust_score": 10,
                "trust_score_rank": 3,
                "trade_vol_24h_btc": 38653.51599269,
                "trade_vol_24h_btc_normalized": 38653.51599269,
                "trade_vol_24h_usd": 2571970939.06,
                "trade_vol_24h_usd_normalized": 2571970939.06,
                "age_of_exchange": 12,
                "ingested_at": "2024-06-17 22:33:10.435522",
            },
        ]
        yield mock


@pytest.fixture
def mock_btc_to_usd_rate():
    with patch("data_pipeline.btc_to_usd_rate") as mock:
        mock.return_value = 50000.00
        yield mock


@pytest.fixture
def mock_loop_through_api():
    with patch("data_pipeline.loop_through_api") as mock:
        mock.return_value = MagicMock(shape=(1, 10))
        yield mock


@pytest.fixture
def mock_data_transformation():
    with patch("data_pipeline.data_transformation") as mock:
        mock.return_value = MagicMock(shape=(1, 15))
        yield mock


@pytest.fixture
def mock_write_to_motherduck_from_data_frame():
    with patch("data_pipeline.write_to_motherduck_from_data_frame") as mock:
        yield mock


def test_run_pipeline(
    mock_get_exchange_data,
    mock_btc_to_usd_rate,
    mock_loop_through_api,
    mock_data_transformation,
    mock_write_to_motherduck_from_data_frame,
):
    """
    Integration test for the run_pipeline function.
    Ensures the pipeline calls get_exchange_data, executes transformations,
    and attempts to write data (
    without actual database interaction due to mocking).
    """
    # Run the pipeline
    run_pipeline()

    # Verify mocked function calls
    mock_get_exchange_data.assert_called_once()
    mock_btc_to_usd_rate.assert_called_once()
    mock_loop_through_api.assert_called_once()
    mock_data_transformation.assert_called_once()
    mock_write_to_motherduck_from_data_frame.assert_called_once()
