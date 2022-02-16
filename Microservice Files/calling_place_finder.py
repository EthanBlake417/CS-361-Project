import json
import os
# arguments can be found at this site:
# https://opentripmap.io/catalog

# step one: start place_finder_api

# query:
with open('input.txt', 'w') as f:
    # zip code, country code, search radius in miles, number of results per argument, arguments
    json.dump(["85282", 'US', 10, "5", ['restaurants', 'interesting_places']], f)

# wait for results:
while True:
    try:
        with open('status.txt', 'r'):
            break
    except FileNotFoundError:
        continue


# results:
with open('output.csv', 'r') as file:
    for row in file:
        print(row)

# delete status.txt
if os.path.exists("status.txt"):
    os.remove("status.txt")