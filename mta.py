import gtfs_realtime_pb2, nyct_subway_pb2
import json, sys, glob

# Data sources
#
# http://data.mytransit.nyc/subway_time/. Has data from Jan 1 2016 until present day
#
# http://web.mta.info/developers/MTA-Subway-Time-historical-data.html. Claims to have data from Sep 17 2014 until present day, but most data is missing.
# Daily dump has 94 days of data starting from Sep 17. 5 min dump has data until Nov 18 2015, but has significant gaps in data.
# Some people have asked about this on the MTA dev mailing list but no one has been able to get a response: https://groups.google.com/forum/#!topic/mtadeveloperresources/9wxXeYwJAMQ.

# Stops with 1 & 2 & 3: Chambers, 14th, 34th, 42nd, 96th.
# Stop id: 635 R20S L03S D13S A31S is 14th (635N/635S)
# Stop id: 12

# TODO: we pretend that arrival time and deperature time are always the same because they're listed as the same
# in most cases. However, they're not always listed as the same. It would be preferable to use real departure and arrival
# times, but we don't have that data so we ignore it in the few cases where do we do have it.

def is_1_train(item):
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

def readable_gtfs_dump(filename):
    feed = get_feed(filename)
    for entity in feed.entity:
        if is_1_train(entity):
            print(entity)

def get_all_stations():
    feed = get_feed('./mta-files/gtfs-2014-09-17-23-41')
    station_ids = set()
    for entity in feed.entity:
        if is_1_train(entity):
            for stop_time in entity.trip_update.stop_time_update:
                station_ids.add(stop_time.stop_id)
    id_to_station = get_stations()
    for station_id in station_ids:
        print(station_id, id_to_station[station_id])

def get_feed(filename):
    feed = gtfs_realtime_pb2.FeedMessage()
    with open(filename,'rb') as f:
        feed.ParseFromString(f.read())
    return feed

def get_files_by_day(day_requested):
    base_file_path = './mta-files/gtfs-'
    day_files = glob.glob(base_file_path + day_requested + "*")
    return day_files


# entity.trip_update.stop_time_update.stop_id
#  Want this to be 635S

# entity.trip_update.trip.route_id
#  Want this to be "1", "2", or "3". Let's say "1".

# readable_gtfs_dump('./mta-files/gtfs-2014-09-17-00-01')
# get_all_stations()

trips = {}

def add_station_time(trips, last_window, trip_id, stop_id, stop_time):
    if stop_id not in trips[trip_id]:
        trips[trip_id][stop_id] = [stop_time]
        return

    if stop_id in last_window or len(trips[trip_id][stop_id]) == 0:
        trips[trip_id][stop_id][-1] = stop_time
    else:
        trips[trip_id][stop_id].append(stop_time)

def get_station_times(filenames):
    changed_direction = set()

    cur_window = set()
    last_window = set()
    for filename in filenames:
        feed = get_feed(filename)
        # debug check to make sure we don't see the same trip_id twice in the same file.
        seen_trip_ids = set()


        for entity in feed.entity:
            # entity is a list of predicted times for a trip Id.
            if is_1_train(entity):
                trip_update = entity.trip_update
                trip_id = trip_update.trip.trip_id
                if trip_id in seen_trip_ids:
                    print('ERROR: saw trip id twice in same file', trip_id)
                    assert(False)

                if trip_id not in trips:
                    trips[trip_id] = {}

                # Check that no trip_id changes direction
                # Trains generally don't change direction, but on rare occasion do
                cur_direction = trip_update.trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor].direction
                if 'direction' in trips[trip_id]:
                    # assert(trips[trip_id]['direction'] == cur_direction)
                    pass
                else:
                    trips[trip_id]['direction'] = cur_direction


                seen_trip_ids.add(trip_id)
                for stop_time in trip_update.stop_time_update:
                    stop_id = stop_time.stop_id
                    cur_window.add(stop_id)

                    # Note sure if this assert is true, but we've never seen it violated
                    arrival_time = stop_time.arrival.time
                    departure_time = stop_time.departure.time

                    if arrival_time != 0:
                        add_station_time(trips, last_window, trip_id, stop_id, arrival_time)
                    elif departure_time != 0:
                        add_station_time(trips, last_window, trip_id, stop_id, departure_time)

                    #
                    if departure_time != 0 and arrival_time != 0:
                        if stop_time.arrival.time != stop_time.departure.time:
                            pass
                            # print(stop_time.stop_id)
                            # We only appear to have a delta for some stations. We don't know why.
                   # assert(arrival_time == 0 or departure_time == 0 or stop_time.arrival.time == stop_time.departure.time)
            last_window = cur_window
    return trips

# select day in yyyy-mm-dd format
day_requested = sys.argv[1]
day_files = get_files_by_day(day_requested)
times = get_station_times(day_files)
print(times)

# for trip_id, station_times in times.items():
#     for station_id, estimated_times in station_times.items():
#         if len(estimated_times) != 1:
#             print(trip_id, station_id, estimated_times)
