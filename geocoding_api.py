# geocoding api
# this takes your zipcode and country code and returns the latitude and longitude
# so that they can be used with the weather_api

import requests


def get_lat_lon(zip_code, country_code="US"):
    """ returns latitude and longitude based on a specific zipcode"""
    api_key = "&appid="+"1cf60e77aaf75d4e7b6dc9982cb83604"
    base = "http://api.openweathermap.org/geo/1.0/zip?zip="
    complete_url = base + zip_code + "," + country_code + api_key
    response = requests.get(complete_url)
    x = response.json()
    return x['lat'], x['lon']


if __name__ == '__main__':
    get_lat_lon(85282, "US")
