import os 
import sys
import logging
import pandas as pd
from datetime import datetime
from extract import get_token_data, btc_to_usd_rate

sys.path.insert(0, './logs/')
from config import log_config  # noqa

log_config()

# Logger for the current module (__name__)
logger = logging.getLogger(__name__)

API_KEY = os.getenv('API_KEY')


# Define the function
def loop_through_api(url: str, headers: dict) -> pd.DataFrame:
    logger.info(f"Fetching data from API: {url}")
    
    try:
        # Fetch data from API
        results = get_token_data(url, headers)
        logger.info("Data fetched successfully from API.")
    except Exception as e:
        logger.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()

    raw_data = []  # Initialize an empty list to store processed data
    for result in results:  # Iterate through each result
        # Check if the result is a dictionary
        if isinstance(result, dict):
            extract = {  # Extract specific fields from the result
                'id': result['id'],
                'name': result['name'],
                'year_established': result['year_established'],
                'country': result['country'],
                'description': result['description'],
                'url': result['url'],
                'has_trading_incentive': result['has_trading_incentive'],
                'trust_score': result['trust_score'],
                'trust_score_rank': result['trust_score_rank'],
                'trade_vol_24h_btc': result['trade_volume_24h_btc'],
                'trade_vol_24h_btc_normalized': result['trade_volume_24h_btc_normalized']
            }
            raw_data.append(extract)  # Add the extracted data to the list
        else:
            # Log non-dict results
            logger.warning(f"Skipping non-dict result: {result}")  
    # Convert the list to a DataFrame and return
    data_ = pd.DataFrame(raw_data)  
    logger.info(
        f'There are {data_.shape[0]} rows & {data_.shape[1]} columns.')

    return data_


def data_transformation(
        df: pd.DataFrame, btc_to_usd_rate: float) -> pd.DataFrame:
    """
    Convert and format the trade volume in BTC to USD.
    Calculate the age of each exchange.

    Args:
        df (pd.DataFrame): The DataFrame containing the trade volume data
        and year established.
        btc_to_usd_rate (float): The current BTC to USD exchange rate.

    Returns:
        pd.DataFrame: The DataFrame with additional columns.
    """
    logger.info("Starting data transformation.")

    # Convert the trade volume to USD
    df['trade_vol_24h_usd_normalized'] = (
        df['trade_vol_24h_btc_normalized'] * btc_to_usd_rate)
    df['trade_vol_24h_usd'] = df['trade_vol_24h_btc'] * btc_to_usd_rate
    logger.debug("Trade volume converted to USD.")

    # Format the USD values for readability
    df['trade_vol_24h_usd'] = df['trade_vol_24h_usd'].apply(
        lambda x: f"{x:.2f}")
    df['trade_vol_24h_usd_normalized'] = (
        df['trade_vol_24h_usd_normalized'].apply(lambda x: f"{x:.2f}"))
    logger.debug("Trade volume formatted for readability.")

    df['age_of_exchange'] = datetime.now().year - df['year_established']
    logger.info("Calculated age of each exchange.")
    logger.info(f'There currently {df.shape[0]} rows & {df.shape[1]} columns.')

    return df


url = 'https://api.coingecko.com/api/v3/exchanges'
headers = {
    'accept': 'application/json',
    'x-cg-pro-api-key': API_KEY
}


# Ensure the btc_to_usd_rate() function is called correctly
btc_rate = btc_to_usd_rate()

data_transformation(loop_through_api(url, headers), btc_rate).to_csv('sample.csv', index=False)
