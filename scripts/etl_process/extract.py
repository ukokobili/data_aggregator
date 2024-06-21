import logging
import sys
import time
from typing import Dict, List

import requests

# Import the config package
sys.path.insert(0, "./logs/")
from config import log_config  # noqa

# Call the log config function
log_config()

# Get logger for the current module (__name__)
logger = logging.getLogger(__name__)


def get_exchange_data(url: str, headers: Dict[str, str]) -> List[Dict]:
    """
    Fetches token data from the provided API endpoint using pagination.

    Args:
        url (str): The URL of the API endpoint.
        headers (dict): The headers to be sent with the GET request.

    Returns:
        list: A list containing all the token data fetched from the API.
    """
    all_data = []
    limit = 100  # Maximum number of results per page
    page = 1  # Current page number

    logger.info(f"Starting to fetch data from {url} with headers: {headers}")

    while True:
        try:
            params = {'per_page': limit, 'page': page}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            logger.info(f"API request returned status: {response.status_code}")

            data = response.json()
            all_data.extend(data)
            logger.info(f"Fetched {len(data)} records from page {page}")

            if len(data) < limit:
                logger.info("No more data to fetch. Exiting loop.")
                break

            page += 1
            logger.info(f"Proceeding to the next page: {page}")
            # Add a delay before the next request
            time.sleep(1)  # Adjust the delay as needed

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                logger.warning(
                    "Rate limit exceeded. Retrying after a delay..."
                )
                time.sleep(60)  # Delay for 60 seconds before retrying
                continue
            logger.error(f"HTTP error occurred: {http_err}")
            break
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
            break

    return all_data


def btc_to_usd_rate() -> float:
    """
    Send a GET request to the API endpoint
    Extract the rate in USD from the response
    Convert to float, round to 2 decimal places, and return
    """
    try:
        logger.info("Fetching BTC to USD rate from CoinCap API")
        response = requests.get("https://api.coincap.io/v2/rates/bitcoin")
        response.raise_for_status()
        rate = round(float(response.json()["data"]["rateUsd"]), 2)
        logger.info(f"Successfully fetched BTC to USD rate: {rate}")
        return rate
    except requests.exceptions.HTTPError as http_err:
        logger.error(
            f"HTTP error occurred while fetching BTC to USD rate: {http_err}"
        )
    except Exception as err:
        logger.error(
            f"An unexpected error occurred fetching BTC to USD rate: {err}"
        )
    return 0.0  # Return a default value in case of error
