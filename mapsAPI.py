import json
import requests
import os


def maps_api_helper(start_lat, start_lon, end_lat, end_lon):
    """helper function for maps_api"""
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyDrUKf_920c0swkWkkNJquund5qDDroeqg'
    nav_request = f'origin={start_lat},{start_lon}&destination={end_lat},{end_lon}&mode=driving&key={api_key}'
    url = endpoint + nav_request

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    with open('directions.txt', 'w') as f:
        f.write(response.text)
        f.close()


def maps_api():
    """ outputs JSON """
    while True:
        try:
            with open('input2.txt', 'r') as f:
                while True:
                    filesize = os.path.getsize("input2.txt")
                    if filesize != 0:
                        break
                args = json.load(f)
                maps_api_helper(args[0], args[1], args[2], args[3])
            with open('status2.txt', 'w') as f:
                f.write("Done")
            if os.path.exists("input2.txt"):
                os.remove("input2.txt")
        except FileNotFoundError:
            continue


if __name__ == '__main__':
    maps_api()