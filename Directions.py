import googlemaps
from datetime import datetime
import json

def guide(src,dst):
    f = open("key.txt", "r")
    key = f.readline()
    gmaps = googlemaps.Client(key=key)
    now = datetime.now()
    directions_result = gmaps.directions(src,dst,mode="walking",departure_time=now)
    return directions_result