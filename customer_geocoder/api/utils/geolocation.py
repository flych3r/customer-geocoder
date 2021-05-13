import os
from typing import Dict

import requests

GEOCODING_API_KEY = os.getenv('GEOCODING_API_KEY')


def lat_lng_by_address(address: str) -> Dict[str, float]:
    """
    Geolocates and address using Google Maps API.

    Parameters
    ----------
    address : str
        string with the address to be geolocated

    Returns
    -------
    dict
        dictionary with lat and lng keys
    """
    payload = {
        'address': address,
        'key': GEOCODING_API_KEY
    }
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(url, params=payload)
    resp_json = response.json()
    return resp_json.get('results')[0].get('geometry').get('location')
