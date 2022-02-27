import requests

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyDrUKf_920c0swkWkkNJquund5qDDroeqg'
origin = input('Where are you?: ').replace(' ', '+')
destination = input('Where do you want to go?: ').replace(' ', '+')
nav_request = 'origin={}&destination={}&mode=driving&key={}'.format(origin,destination,api_key)  
url = endpoint +nav_request

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

with open('directions.txt','w') as f:
    f.write(response.text)
    f.close()
##print(response.text)

