import requests
import time
from forex_python.converter import CurrencyRates
from datetime import datetime

bitcoin_api_url = 'https://api.cryptonator.com/api/ticker/btc-usd'
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/b4aJ6LJX9kedZfoyCLtCqw'
bitcoin_lower_threshold = 200000
bitcoin_upper_threshold = 400000  

def get_latest_bitcoin_price():
    response = requests.get(bitcoin_api_url, headers={'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'})
    response_json = response.json()

    return float(response_json['ticker']['price'])

def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desired event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Sends a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)

def convert_to_rands(price_usd):
    # Note you can get the bitcoin price 
    # directly by using BtcConverter()
    rates = CurrencyRates()
    usd_to_zar = rates.get_rates('USD')['ZAR']
    price_rand = price_usd * usd_to_zar
    print(price_rand)
    return price_rand

def main():
    
    while True:
        price_usd = get_latest_bitcoin_price()
        price_rand = convert_to_rands(price_usd)

        # Send an emergency notification
        if price_rand < bitcoin_lower_threshold or price_rand > bitcoin_upper_threshold:
            post_ifttt_webhook('bitcoin_price_emergency', price_rand)

        # Sleep for 10 minutes 
        time.sleep(10 * 60)

if __name__ == '__main__':
    main()

