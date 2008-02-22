# -*- coding: utf-8 -*-

import time, datetime
from lib import i18n

SC_ONCE = _("Once")
SC_WEEKLY = _("Weekly")
SC_MONTHLY = _("Monthly")

def time_from_calendar(calendar):
    ''' Return a time object representing the date. '''
    day = calendar[2]
    month = calendar[1] + 1
    year = calendar[0]
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

def get_schedule_timestamp(frequency, date):
    ''' Return the scheduled date from original date. '''

    # Date conversion if needed
    if isinstance(date, float):
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
    ''' Return the timestamp for the first day of the given month. '''
    ret = datetime.datetime(year, month, 1, 0, 0, 0)

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def last_of_month(month, year):
    ''' Return the timestamp for the last day of the given month. '''
    nextMonth = month % 12 + 1
    goback = datetime.timedelta(seconds=1)
    # Create datetime object with a timestamp corresponding the end of day
    nextMonth = datetime.datetime(year, nextMonth, 1, 0, 0, 0)
    ret = nextMonth - goback

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def get_alarm_timestamp(alertDays, alertTime, origDate=None):
    ''' Calculate alarm timestamp. '''

    if not origDate:
        origDate = datetime_from_timestamp(origDate)
    elif isinstance(origDate, float):
        origDate = datetime_from_timestamp(origDate)

    alertTime = alertTime.split(':')
    delta = datetime.timedelta(days=alertDays)
    alertDate = origDate - delta

    ret = datetime.datetime(alertDate.year, alertDate.month, alertDate.day, int(alertTime[0]), int(alertTime[1]))

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret
