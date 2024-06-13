import logging
import os
import sys

import duckdb

sys.path.insert(0, './logs/')
from config import log_config  # noqa

# Call the log_config function
log_config()
# Logger for the current module (__name__)
logger = logging.getLogger(__name__)

# Import data warehouse variables
database_name = os.getenv('DATABASE_NAME')
motherduck_token = os.getenv('MOTHERDUCK_TOKEN')


def write_to_motherduck_from_data_frame(data_frame):
    """
    Writes the DataFrame to a MotherDuck database table named 'tokens'.
    If there are conflicts on 'exchangeId', 
    the existing records are updated with the new data.

    Args:
        data_frame (pd.DataFrame): The DataFrame containing 
        the data to be written to the database.

    Returns:
        None
    """
    logger.info("Starting to write DataFrame to MotherDuck")

    try:
        logger.debug(f"Connecting to MotherDuck database: {database_name}")  
        with duckdb.connect(
            f'md:{database_name}?motherduck_token={motherduck_token}'
        ) as con:
            logger.debug("Executing SQL insert/update command")
            con.sql(
                f"""
                INSERT INTO tokens
                SELECT * FROM {'data_frame'}
                ON CONFLICT (exchangeId) DO UPDATE SET
                name = EXCLUDED.name,
                rank = EXCLUDED.rank,
                percentTotalVolume = EXCLUDED.percentTotalVolume,
                volumeUsd = EXCLUDED.volumeUsd,
                tradingPairs = EXCLUDED.tradingPairs,
                socket = EXCLUDED.socket,
                exchangeUrl = EXCLUDED.exchangeUrl,
                updated = EXCLUDED.updated,
                updated_at = EXCLUDED.updated_at;
                """
            )
        logger.info('Successfully wrote to MotherDuck')
    except duckdb.Error as e:
        logger.error(f"Error writing to MotherDuck: {e}")

logger.info("Data warehouse variables loaded successfully")
