import logging
import os
import sys

import duckdb

sys.path.insert(0, "./logs/")
from config import log_config  # noqa

# Call the log_config function
log_config()
# Logger for the current module (__name__)
logger = logging.getLogger(__name__)

# Import data warehouse variables
database_name = os.getenv("DATABASE_NAME")
motherduck_token = os.getenv("MOTHERDUCK_TOKEN")


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

        with duckdb.connect(
            f"md:{database_name}?motherduck_token={motherduck_token}"
        ) as con:
            logger.debug("Executing SQL insert/update command")
            con.sql(
                f"""
        INSERT INTO exchange
        SELECT * FROM {'data_frame'}
        ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        year_established = EXCLUDED.year_established,
        country = EXCLUDED.country,
        description = EXCLUDED.description,
        url = EXCLUDED.url,
        has_trading_incentive = EXCLUDED.has_trading_incentive,
        trust_score = EXCLUDED.trust_score,
        trust_score_rank = EXCLUDED.trust_score_rank,
        trade_vol_24h_btc = EXCLUDED.trade_vol_24h_btc,
        trade_vol_24h_btc_normalized=EXCLUDED.trade_vol_24h_btc_normalized,
        trade_vol_24h_usd = EXCLUDED.trade_vol_24h_usd,
        trade_vol_24h_usd_normalized=EXCLUDED.trade_vol_24h_usd_normalized,
        age_of_exchange = EXCLUDED.age_of_exchange,
        ingested_at = EXCLUDED.ingested_at;
                """
            )
    except duckdb.Error as e:
        logger.error(f"Error writing to MotherDuck: {e}")
