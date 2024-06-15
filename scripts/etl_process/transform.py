import sys
import logging
import numpy as np
import pandas as pd
from datetime import datetime

sys.path.insert(0, './logs/')
from config import log_config  # noqa

log_config()

# Logger for the current module (__name__)
logger = logging.getLogger(__name__)


# Define the function
def loop_through_api(api_raw_data: pd.DataFrame) -> pd.DataFrame:
    
    try:
        # Fetch data from API
        results = api_raw_data
        logger.info("Data fetched successfully from API.")
    except Exception as e:
        logger.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()

    raw_data = []  # Initialize an empty list to store processed data
    for result in results:  # Iterate through each result
        # Check if the result is a dictionary
        if isinstance(result, dict):
            extract = { # Extract specific fields from the result
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

    return data_

def convert_to_int(x):
    # Convert to float first to handle strings
    if pd.notna(x):
        return int(float(x))  
    else:
        return np.nan
    

def data_transformation(
        df: pd.DataFrame, btc_to_usd_rate: float) -> pd.DataFrame:
    """
    Convert and format the trade volume in BTC to USD.
    Calculate the age of each exchange.
    Ingested date and time

    Args:
        df (pd.DataFrame): The DataFrame containing the trade volume data
        and year established.
        btc_to_usd_rate (float): The current BTC to USD exchange rate.

    Returns:
        pd.DataFrame: The DataFrame with additional columns.
    """

    # Convert the trade volume to USD
    df['trade_vol_24h_usd'] = df['trade_vol_24h_btc'] * btc_to_usd_rate
    df['trade_vol_24h_usd_normalized'] = (
        df['trade_vol_24h_btc_normalized'] * btc_to_usd_rate)

    # Format the USD values for readability
    df['trade_vol_24h_usd'] = df['trade_vol_24h_usd'].apply(
        lambda x: f"{x:.2f}")
    df['trade_vol_24h_usd_normalized'] = (
        df['trade_vol_24h_usd_normalized'].apply(lambda x: f"{x:.2f}"))

    df['age_of_exchange'] = datetime.now().year - df['year_established']
    
    df['ingested_at'] = datetime.now()

    # convert from float to int
    df['age_of_exchange'] = df['age_of_exchange'].apply(convert_to_int)
    df['year_established'] = df['year_established'].apply(convert_to_int)
    df['trust_score'] = df['trust_score'].apply(convert_to_int)
    df['trust_score_rank'] = df['trust_score_rank'].apply(convert_to_int)
    
    return df


