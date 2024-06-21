import os
import sys

import pytest

sys.path.append("./scripts")
from etl_process.extract import get_exchange_data  # noqa

API_KEY = os.getenv("API_KEY")

# API URL and API KEY authentication
url = "https://api.coingecko.com/api/v3/exchanges"
headers = {"accept": "application/json", "x-cg-pro-api-key": API_KEY}


@pytest.fixture
def api_response():
    result = get_exchange_data(url, headers)
    return result


# def test_api_returns_list(api_response):
#     assert isinstance(api_response, list), 'Data is not a list!'

#     # Assert list is not empty
#     assert len(api_response) > 0, "API returned an empty list!"


def test_api_returns_expected_data(api_response):
    """
    Test to check if the API response contains data for specific exchanges.

    Args:
      api_response (list): The data returned from the API.
    """
    # Define expected exchange IDs
    expected_ids = [
        "binance",
        "bybit_spot",
        "huobi",
        "gdax",
        "gate",
        "kucoin",
        "kraken",
        "bitfinex",
        "hashkey-global",
        "hashkey_exchange",
        "binance_us",
    ]

    # Check if any exchange in the response has an ID in the expected list
    found_expected = any(
        exchange["id"] in expected_ids for exchange in api_response
    )

    assert found_expected, "API doesn't contain data for expected exchanges!"
