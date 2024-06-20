import os
import sys
import requests
import pytest

sys.path.append('./scripts')
from etl_process.transform import get_exchange_data, data_transformation

API_KEY = os.getenv('API_KEY')

# API URL and API KEY authentication
url = 'https://api.coingecko.com/api/v3/exchanges'
headers = {
    'accept': 'application/json',
    'x-cg-pro-api-key': API_KEY
}

@pytest.fixture
def get_response():
    result = get_exchange_data(url, headers)
    return result


@pytest.mark.parametrize(
    "column_name, expected_type",
    [
        ("id", int),
        ("name", str),
        ("year_established", int),
        ("country", str),
        ("description", str),
        ("url", str),
        ("has_trading_incentive", bool),
        ("trust_score", int),
        ("trust_score_rank", int),
        ("trade_vol_24h_btc", float),
        ("trade_vol_24h_btc_normalized", float),
        ("trade_vol_24h_usd", float),
        ("trade_vol_24h_usd_normalized", float),
        ("age_of_exchange", int),
        ("ingested_at", )

    ],
)
def test_dataframe_dtypes(column_name, expected_type):
  """
  Parametrized test to check data types in each column.

  Args:
      column_name (str): Name of the column to test.
      expected_type (type): Expected data type for the column.
  """
  df = get_response()
  assert df[column_name].dtype == expected_type, f"Column '{column_name}' has incorrect data type!"


def test_dataframe_missing_values():
  """
  Test to check for missing values (NaN or None) in the DataFrame.
  """
  df = get_response()
  assert df.isnull().sum().sum() > 0, "No missing values found in the DataFrame!"
  # You can add further assertions to check for missing values in specific columns if needed.