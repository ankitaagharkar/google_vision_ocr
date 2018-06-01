import googlemaps
gmaps = googlemaps.Client(key='AIzaSyC7SQ-1m0M6dN9L4E2aUhTM1ihAfTXIA0k ')
json_val = gmaps.geocode("629 10th Ave Prospect Park PA 19076 USA")
print(json_val)