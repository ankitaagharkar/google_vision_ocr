import googlemaps
gmaps = googlemaps.Client(key='AIzaSyC7SQ-1m0M6dN9L4E2aUhTM1ihAfTXIA0k ')
json_val = gmaps.geocode("7886 ONTARIO ST VANCOUVER BC")
print(json_val)