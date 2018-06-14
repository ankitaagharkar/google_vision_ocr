import googlemaps
gmaps = googlemaps.Client(key='AIzaSyCao8hUleolUVnfFVI3CmBHECSbO1FZFpg')
json_val = gmaps.geocode("0840 Y414-H155 ST AUGUSTINE'S PARISH SCHOOL EAGLE PARK OSSINING NY 10562-0000")
print(json_val)