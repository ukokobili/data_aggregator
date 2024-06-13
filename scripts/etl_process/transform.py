import os 
import pandas as pd
from extract import get_token_data

API_KEY = os.getenv('API_Key')

# Define the function
def loop_through_api():  
  # Fetch data from API
  results = get_token_data(url, headers)  

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
        'trade_volume_24h_btc': result['trade_volume_24h_btc'],
        'trade_volume_24h_btc_normalized': result['trade_volume_24h_btc_normalized']
      }
      raw_data.append(extract)  # Add the extracted data to the list
    else:
      print(f"Skipping non-dict result: {result}")  # Log non-dict results

  return pd.DataFrame(raw_data)  # Convert the list to a DataFrame and return

url = 'https://api.coingecko.com/api/v3/exchanges'
headers = {
    'accept': 'application/json',
    'x-cg-pro-api-key': API_KEY
}

loop_through_api().to_csv('sample.csv', index=False)