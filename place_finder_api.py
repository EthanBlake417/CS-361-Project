# Ethan Blake
# CS 361
# This is my placefinder microservice. In order to use it, use an input.txt file and an output.txt file


import json
import pandas as pd
import requests
from geocoding_api import get_lat_lon
import random
import os


def miles_to_meters(num_in_miles):
    """ Converts miles to meters """
    return str(num_in_miles*1609.34)


def key_error_edit(num_results, xid_list, list_of_dicts, api_key):
    """
    takes a list of dicts and checks for each category if there is an error,
    in which case it just puts None.
    Helper function for get_places_by_radius
    """
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
    return list_of_dicts


def get_places_by_radius(zip_code, country_code, mile_radius, num_results, kinds):
    list_of_dicts = []
    lat, lon = get_lat_lon(str(zip_code), str(country_code))
    base = "https://api.opentripmap.com/0.1/"
    lang = "en"
    api_key = "5ae2e3f221c38a28845f05b6a03ffaf9c16c2f25fa395ff1c5e761c9"
    response = requests.get(f"{base}{lang}/places/radius?radius={miles_to_meters(mile_radius)}&lon={lon}&lat={lat}&kinds={kinds}&limit={100}&apikey={api_key}").json()
    # get random results from the 100 results
    xid_list = []
    try:
        for i in range(100):
            if response['features'][i]['properties']['name'] != '':
                xid_list.append(response['features'][i]['properties']['xid'])
    except Exception:
        pass
    # shuffle the results
    random.shuffle(xid_list)
    key_error_edit(num_results, xid_list, list_of_dicts, api_key)
    return list_of_dicts, lat, lon


def make_csv(zip_code, country_code, mile_radius, num_results, kinds: list):
    """ This function makes a csv file with the information"""
    list_of_dicts, name, city, state, url = [], [], [], [], []
    wikipedia, latitude, longitude, kinds_list, distance = [], [], [], [], []
    for i in range(len(kinds)):
        place, og_lat, og_lon = get_places_by_radius(zip_code, country_code, mile_radius, int(num_results), kinds[i])
        list_of_dicts.append(place)
    for i in range(len(list_of_dicts)):
        for j in range(len(list_of_dicts[i])):
            name.append(list_of_dicts[i][j]['name']), city.append(list_of_dicts[i][j]['city'])
            state.append(list_of_dicts[i][j]['state']), url.append(list_of_dicts[i][j]['url'])
            wikipedia.append(list_of_dicts[i][j]['wikipedia']), kinds_list.append(list_of_dicts[i][j]['kinds'])
            latitude.append(list_of_dicts[i][j]['lat_long']['lat']), longitude.append(list_of_dicts[i][j]['lat_long']['lon'])
    df = pd.DataFrame()
    df['name'], df['city'], df['state'], df['website'] = name, city, state, url
    df['wikipedia'], df['type_of_activity'], df['latitude'], df['longitude'] = wikipedia, kinds_list, latitude, longitude
    df.to_csv('output.csv', index=False)


def place_finder():
    """ This function finds places by calling an API, and then formats the information in a CSV file."""
    while True:
        try:
            with open('input.txt', 'r') as f:
                while True:
                    filesize = os.path.getsize("input.txt")
                    if filesize != 0:
                        break
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
