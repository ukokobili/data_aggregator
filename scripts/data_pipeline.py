import os
import sys
import logging
from datetime import datetime
from etl_process.extract import get_exchange_data #, btc_to_usd_rate
from etl_process.transform import loop_through_api, data_transformation
from etl_process.load import write_to_motherduck_from_data_frame

API_KEY = os.getenv('API_KEY')

sys.path.insert(0, './logs/')
from config import log_config  # noqa

log_config()

# Logger for the current module (__name__)
logger = logging.getLogger(__name__)

# api url and API KEY authentication
url = 'https://api.coingecko.com/api/v3/exchanges'
headers = {
    'accept': 'application/json',
    'x-cg-pro-api-key': API_KEY
}

#btc_rate = btc_to_usd_rate()


# function to run the entire pipeline
def run_pipeline() -> None:
    try:
        # pipeline start time
        pipeline_start_time = datetime.now()

        # catch exhange data from Coingeko API
        catch_api_data = get_exchange_data(url, headers)
        catch_api_data
        # transform data into a structured table
        # structure_the_data = loop_through_api(catch_api_data)
        # # convert btc to usd, convert datatypes, add additional columns
        # clean_transform_data = data_transformation(structure_the_data,
        #                                             btc_rate)
        # load data warehouse 
        # write_to_motherduck_from_data_frame(
        #     clean_transform_data
        # )
    
    except Exception as err:
        logger.error(f'Error running pipeline: {err}')


    if __name__=='__main__':
        run_pipeline()
