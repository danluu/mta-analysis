# According to http://web.mta.info/developers/MTA-Subway-Time-historical-data.html, the MTA has archived historical data starting from 9/17/2014 until present day.
# However, it appears that most of the files are missing: https://groups.google.com/forum/#!topic/mtadeveloperresources/9wxXeYwJAMQ.
# This script attempts to grab the files that actually exist, whatever they are.

from datetime import timedelta, date

def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def within_day_range():
    for hour in range(0, 24):
        for minute in range(1, 57, 5):
            yield "{0:02d}-{1:02d}".format(hour, minute)

start_date = date(2014, 9, 17)
end_date = date(2017, 6, 21)

# for a_date in date_range(start_date, end_date):
#     date_str = a_date.strftime("%Y-%m-%d")
#     url = 'https://datamine-{}.s3.amazonaws.com/gtfs.tgz'.format(date_str)

for a_date in date_range(start_date, end_date):
    for within_day in within_day_range():
        ymd = a_date.strftime("%Y-%m-%d")
        url = 'https://datamine-history.s3.amazonaws.com/gtfs-{}-{}'.format(ymd, within_day)
        print(url)


