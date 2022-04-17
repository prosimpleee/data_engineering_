import pandas as pd
import requests
from datetime import datetime


def extract_covid_statistics():
    token = '154bf7d4f489cf9b32095b31'
    url = 'https://v6.exchangerate-api.com/v6/{}/latest/USD'.format(token)
    response = requests.get(url)
    data = response.json()
    
    
    list_currency = [{'CurrencyName': base,
                      'Value': value} for base, value in data['conversion_rates'].items() if
                       base in ('EUR', 'USD', 'GBP')]
    df = pd.DataFrame(list_currency)
    df['CreatedTimestamp'] = datetime.strptime(data['time_last_update_utc'], '%a, %d %b %Y %H:%M:%S +%f')
    
    print(df)
    
extract_covid_statistics()