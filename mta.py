import gtfs_realtime_pb2, nyct_subway_pb2
import json

# Stops with 1 & 2 & 3: Chambers, 14th, 34th, 42nd, 96th.
# Stop id: 635 R20S L03S D13S A31S is 14th (635N/635S)
# Stop id: 12

# TODO: make this less... bad.
# TODO: note that this doesn't check for the station.
def is_1_train_at_14th_south(item):
    if not item.HasField('trip_update'):
        return False
    if not item.trip_update.HasField('trip'):
        return False
    if item.trip_update.trip.route_id != '1':
        return False
    return True

def get_stations():
    with open('mta-files/stations.json') as s:
        stations = json.load(s)
    id_to_station = {}
    for station in stations['result']:
        id_to_station.update({station['id']: station['name']})
    return id_to_station

feed = gtfs_realtime_pb2.FeedMessage()
with open('./mta-files/gtfs-2014-09-17-23-41','rb') as f:
    feed.ParseFromString(f.read())
station_ids = set()
for entity in feed.entity:
    if is_1_train_at_14th_south(entity):
        for stop_time in entity.trip_update.stop_time_update:
            station_ids.add(stop_time.stop_id)
id_to_station = get_stations()
for station_id in station_ids:
    print(station_id, id_to_station[station_id])


# entity.trip_update.stop_time_update.stop_id
#  Want this to be 635S

# entity.trip_update.trip.route_id
#  Want this to be "1", "2", or "3". Let's say "1".
