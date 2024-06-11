import os
import sys
import logging
import requests
from typing import Dict, List

# Import the config package
sys.path.insert(0, './logs/')
from config import log_config

API_KEY = os.getenv('API_Key')

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

        except Exception as err:
            logger.error(f'An unexpected error occurred: {err}')
            break

    return all_data

url = 'https://api.coingecko.com/api/v3/exchanges'
headers = {
    'accept': 'application/json',
    'x-cg-pro-api-key': API_KEY
}

get_token_data(url, headers)
