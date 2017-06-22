import gtfs_realtime_pb2, nyct_subway_pb2
import requests

# Stops with 1 & 2 & 3: Chambers, 14th, 34th, 42nd, 96th.
# Stop id: 635 R20S L03S D13S A31S is 14th (635N/635S)
# Stop id: 12

# TODO: make this less... bad.
# TODO: note that this doesn't check for the station.
def is_1_train_at_14th_south():
    if item.HasField('trip_update'):
        if item.trip_update.HasField('trip'):
            if item.trip_update.trip.route_id != '1':
                return False
        else:
            return False
    else:
        return False
    return True


feed = gtfs_realtime_pb2.FeedMessage()
with open('/Users/danluu/Downloads/gtfs/gtfs-2014-09-17-23-41','rb') as f:
    feed.ParseFromString(f.read())
    for item in feed.entity:
        if is_1_train_at_14th_south():
            print(item)

# entity.trip_update.stop_time_update.stop_id
#  Want this to be 635S

# entity.trip_update.trip.route_id
#  Want this to be "1", "2", or "3". Let's say "1".

