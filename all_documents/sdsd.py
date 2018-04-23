import googlemaps

gmaps = googlemaps.Client(key='AIzaSyC7SQ-1m0M6dN9L4E2aUhTM1ihAfTXIA0k ')
json_val = gmaps.geocode('2323 Ross Avenue, Suite 1400 Dallas TX 75201-2721')
print(json_val)