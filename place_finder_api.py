# Ethan Blake
# CS 361
# This is my placefinder microservice. In order to use it, use an input.txt file and an output.txt file


import json
import time
import pandas as pd
import requests
from geocoding_api import get_lat_lon
import random
import os


def miles_to_meters(num_in_miles):
    return str(num_in_miles*1609.34)


def get_places_by_radius(zip_code, country_code, mile_radius, num_results, kinds):
    list_of_dicts = []
    # for search by radius
    # zip_code = input("Please enter your zip code: ")
    # country_code = input("Please enter your country code: ")
    lat, lon = get_lat_lon(str(zip_code), str(country_code))
    base = "https://api.opentripmap.com/0.1/"
    lang = "en"
    # mile_radius = 10
    # lon = "-112.07404"
    # lat = "33.44838"
    api_key = "5ae2e3f221c38a28845f05b6a03ffaf9c16c2f25fa395ff1c5e761c9"
    # num_results = "100"
    # kinds = "amusements"
    # response = requests.get("https://api.opentripmap.com/0.1/en/places/geoname?name=Phoenix&country=US&apikey=5ae2e3f221c38a28845f05b6a03ffaf9c16c2f25fa395ff1c5e761c9")
    response = requests.get(f"{base}{lang}/places/radius?radius={miles_to_meters(mile_radius)}&lon={lon}&lat={lat}&kinds={kinds}&limit={100}&apikey={api_key}").json()
    # print(response.status_code)
    # get random results from the 100 results
    xid_list = []
    try:
        for i in range(100):
            if response['features'][i]['properties']['name'] != '':
                xid_list.append(response['features'][i]['properties']['xid'])
    except Exception:
        pass
    random.shuffle(xid_list)
    try:
        for i in range(int(num_results)):
            xid = xid_list[i]
            new_response = requests.get(f"https://api.opentripmap.com/0.1/en/places/xid/{xid}?apikey={api_key}").json()
            # print(new_response)
            return_dict = {}
            try:
                return_dict['name'] = new_response['name']
            except KeyError:
                return_dict['name'] = None
            try:
                return_dict['city'] = new_response['address']['city']
            except KeyError:
                return_dict['city'] = None
            try:
                return_dict['state'] = new_response['address']['state']
            except KeyError:
                return_dict['state'] = None
            try:
                return_dict['url'] = new_response['url']
            except KeyError:
                return_dict['url'] = None
            try:
                return_dict['wikipedia'] = new_response['wikipedia']
            except KeyError:
                return_dict['wikipedia'] = None
            try:
                return_dict['kinds'] = new_response['kinds']
            except KeyError:
                return_dict['kinds'] = None
            try:
                return_dict['lat_long'] = new_response['point']
            except KeyError:
                return_dict['lat_long'] = None
            list_of_dicts.append(return_dict)
    except IndexError:
        pass
    return list_of_dicts, lat, lon


def make_csv(zip_code, country_code, mile_radius, num_results, kinds: list):
    list_of_dicts = []
    name = []
    city = []
    state = []
    url = []
    wikipedia = []
    latitude = []
    longitude = []
    kinds_list = []
    distance = []
    for i in range(len(kinds)):
        place, og_lat, og_lon = get_places_by_radius(zip_code, country_code, mile_radius, int(num_results), kinds[i])
        list_of_dicts.append(place)
    for i in range(len(list_of_dicts)):
        for j in range(len(list_of_dicts[i])):
            name.append(list_of_dicts[i][j]['name'])
            city.append(list_of_dicts[i][j]['city'])
            state.append(list_of_dicts[i][j]['state'])
            url.append(list_of_dicts[i][j]['url'])
            wikipedia.append(list_of_dicts[i][j]['wikipedia'])
            kinds_list.append(list_of_dicts[i][j]['kinds'])
            latitude.append(list_of_dicts[i][j]['lat_long']['lat'])
            longitude.append(list_of_dicts[i][j]['lat_long']['lon'])
            distance.append(15)
    df = pd.DataFrame()
    df['name'] = name
    df['city'] = city
    df['state'] = state
    df['website'] = url
    df['wikipedia'] = wikipedia
    df['type_of_activity'] = kinds_list
    df['latitude'] = latitude
    df['longitude'] = longitude
    df['distance'] = distance
    df.to_csv('output.csv', index=False)


def place_finder():
    while True:
        try:
            with open('input.txt', 'r') as f:
                time.sleep(2)
                args = json.load(f)
                make_csv(str(args[0]), str(args[1]), int(args[2]), str(args[3]), args[4])
            with open('status.txt', 'w') as f:
                f.write("Done")
            if os.path.exists("input.txt"):
                os.remove("input.txt")
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    place_finder()
