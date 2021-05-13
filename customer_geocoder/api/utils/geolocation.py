import os
import requests

GEOCODING_API_KEY = os.getenv('GEOCODING_API_KEY')


def lat_lng_by_address(address):
    payload = {
        'address': address,
        'key': GEOCODING_API_KEY
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(url, params=payload)
    resp_json = response.json()
    return resp_json.get('results')[0].get('geometry').get('location')
