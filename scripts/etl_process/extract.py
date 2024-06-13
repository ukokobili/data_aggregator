import sys
import logging
import requests
import time
from typing import Dict, List

# Import the config package
sys.path.insert(0, './logs/')
from config import log_config

# Call the log config function
log_config()

# Get logger for the current module (__name__)
logger = logging.getLogger(__name__)

def get_token_data(url: str, headers: Dict[str, str]) -> List[Dict]:
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

    while True:
        try:
            paginated_url = f"{url}?per_page={limit}&page={page}"
            response = requests.get(paginated_url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            logger.info(f'API request status: {response.status_code}')
            
            data = response.json()
            all_data.extend(data)

            if len(data) < limit:
                break

            page += 1
            # Add a delay before the next request
            time.sleep(1)  # Adjust the delay as needed

        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:
                logger.warning('Rate limit exceeded. Retrying after a delay...')
                time.sleep(60)  # Delay for 60 seconds before retrying
                continue
            logger.error(f'HTTP error occurred: {http_err}')
            break
        except Exception as err:
            logger.error(f'An unexpected error occurred: {err}')
            break

    return all_data


def btc_usd_current_price() -> float:
    """
    Send a GET request to the API endpoint
    Extract the rate in USD from the response
    Convert to float, round to 2 decimal places, and return
    """
    response = requests.get('https://api.coincap.io/v2/rates/bitcoin')
    return round(float(response.json()['data']['rateUsd']), 2)
