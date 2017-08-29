# http://data.mytransit.nyc.s3.amazonaws.com/subway_time/2016/2016-02/subway_time_20160201.tar.xz
# http://data.mytransit.nyc.s3.amazonaws.com/subway_time/2016/2016-03/subway_time_20160301.tar.xz
# http://data.mytransit.nyc.s3.amazonaws.com/subway_time/2016/2016-04/subway_time_20160401.tar.xz

import datetime

day = datetime.date(2016,1,1)
for i in range(516):
    day += datetime.timedelta(days=1)
    url = "http://data.mytransit.nyc.s3.amazonaws.com/subway_time/{}/{}-{:0>2}/subway_time_{}{:0>2}{:0>2}.tar.xz".format(
        day.year, day.year, day.month, day.year, day.month, day.day)
    print(url)
