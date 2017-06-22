import gtfs_realtime_pb2, nyct_subway_pb2
import requests

# Stops with 1 & 2 & 3: Chambers, 14th, 34th, 42nd, 96th.
# Stop id: 635 is 14th (635N/635S)

feed = gtfs_realtime_pb2.FeedMessage()
with open('/Users/danluu/Downloads/gtfs/gtfs-2014-09-17-23-41','rb') as f:
    feed.ParseFromString(f.read())
    print(feed)


