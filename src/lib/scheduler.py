# -*- coding: utf-8 -*-

import time, datetime
from lib import i18n

SC_ONCE = _("Once")
SC_WEEKLY = _("Weekly")
SC_MONTHLY = _("Monthly")

def time_from_calendar(calendar):
    ''' Return a time object representing the date. '''
    day = self.calendar.get_date()[2]
    month = self.calendar.get_date()[1] + 1
    year = self.calendar.get_date()[0]
    # Create datetime object
    ret = datetime.datetime(year, month, day)
    # Convert from datetime to time
    ret = timestamp_from_datetime(ret)

    return ret

def timestamp_from_datetime(date):
    ''' Convert a datetime object into a time object. '''
    if isinstance(date, datetime.datetime):
        ret = time.mktime(date.timetuple())
    else:
        ret = time.time()

    return ret

def datetime_from_timestamp(timestamp):
    ''' Convert a time object into a datetime object. '''
    if isinstance(timestamp, float):
        ret = datetime.datetime.fromtimestamp(timestamp)
    else:
        ret = datetime.datetime.now()

    return ret

def get_schedule_date(frequency, date):
    ''' Return the scheduled date from original date. '''

    # Date conversion if needed
    if isinstance(timestamp, float):
        date = datetime_from_timestamp(date)

    if frequency == SC_WEEKLY:
        delta = datetime.timedelta(days=7)
        ret = date + delta
    elif frequency == SC_MONTHLY:
        nextMonth = date.month % 12 + 1
        ret = datetime.datetime(date.year, nextMonth, date.day)
    else:
        ret = date

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def first_of_month(month, year):
    ret = datetime.datetime(year, month, 1, 0, 0, 0)

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def last_of_month(month, year):
    nextMonth = month % 12 + 1
    goback = datetime.timedelta(seconds=1)
    # Create datetime object with a timestamp corresponding the end of day
    nextMonth = datetime.datetime(year, nextMonth, 1, 0, 0, 0)
    ret = nextMonth - goback

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret
