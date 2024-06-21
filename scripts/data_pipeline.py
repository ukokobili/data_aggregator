import logging
import os
import sys
from datetime import datetime

from etl_process.extract import btc_to_usd_rate, get_exchange_data
from etl_process.load import write_to_motherduck_from_data_frame
from etl_process.transform import data_transformation, loop_through_api

API_KEY = os.getenv("API_KEY")

sys.path.insert(0, "./logs/")
from config import log_config  # noqa

log_config()

# Logger for the current module (__name__)
logger = logging.getLogger(__name__)

# API URL and API KEY authentication
url = "https://api.coingecko.com/api/v3/exchanges"
headers = {"accept": "application/json", "x-cg-pro-api-key": API_KEY}


def run_pipeline() -> None:
    """
    Run the entire ETL pipeline: extraction, transformation, and loading.
    This function fetches exchange data from the CoinGecko API,
    transforms the data,
    converts BTC to USD, and loads the cleaned data into a data warehouse.

    Args:
        None

    Returns:
        None
    """
    try:
        # Pipeline start time
        pipeline_start_time = datetime.now()
        logger.info(f"Pipeline started at {pipeline_start_time}")

        # Fetch exchange data from CoinGecko API
        logger.info("Fetching exchange data from CoinGecko API")
        exchange_data = get_exchange_data(url, headers)
        logger.info(f"Fetched exchange data: {len(exchange_data)} records")

        # Transform data into a structured table
        logger.info("Transforming exchange data")
        structured_data = loop_through_api(exchange_data)
        logger.info(
            f"Transformed complete, table: {structured_data.shape[0]} rows"
        )

        # Convert BTC to USD, convert datatypes, add additional columns
        logger.info(
            "Converting BTC to USD and performing additional transformations"
        )
        btc_rate = btc_to_usd_rate()  # Moved inside the function
        cleaned_data = data_transformation(structured_data, btc_rate)
        logger.info("Data transformation complete.")
        logger.info(
            f" {cleaned_data.shape[0]} rows & {cleaned_data.shape[1]} columns."
        )

        # Load data into data warehouse
        logger.info("Loading data into data warehouse")
        write_to_motherduck_from_data_frame(cleaned_data)
        logger.info("Data successfully loaded into MotherDuck")

        pipeline_end_time = datetime.now()
        logger.info(
            f"Pipeline completed successfully at {pipeline_end_time}."
            f"Total time: {pipeline_end_time - pipeline_start_time}"
        )

    except Exception as err:
        logger.error(f"Error running pipeline: {err}")


if __name__ == "__main__":
    run_pipeline()
