import requests


def maps_api(start_lat, start_lon, end_lat, end_lon):
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyDrUKf_920c0swkWkkNJquund5qDDroeqg'
    origin = start_lat, start_lon
    destination = end_lat, end_lon
    origin = str(origin).replace(' ', '')
    destination = str(destination).replace(' ', '')
    # print(origin, destination)
    # origin = input('Where are you?: ').replace(' ', '+')
    # destination = input('Where do you want to go?: ').replace(' ', '+')
    nav_request = f'origin={start_lat},{start_lon}&destination={end_lat},{end_lon}&mode=driving&key={api_key}'
    url = endpoint + nav_request

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    with open('directions3.txt', 'w') as f:
        f.write(response.text)
        f.close()
    ##print(response.text)


if __name__ == '__main__':
    maps_api(33.393356, -111.912445, 33.334148, -111.910545)
