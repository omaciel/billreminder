# -*- coding: utf-8 -*-

import time, datetime
from lib import i18n

SC_ONCE = _("Once")
SC_WEEKLY = _("Weekly")
SC_MONTHLY = _("Monthly")

MULTIPLIER = {
    SC_ONCE: 0,
    SC_WEEKLY: 7,
    SC_MONTHLY: 30
}

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
    if isinstance(date, (datetime.datetime, datetime.date)):
        ret = time.mktime(date.timetuple())
    else:
        ret = time.time()

    return int(ret)

def datetime_from_timestamp(timestamp):
    ''' Convert a time object into a datetime object. '''
    if isinstance(timestamp, float) or isinstance(timestamp, int):
        ret = datetime.datetime.fromtimestamp(timestamp)
    else:
        ret = datetime.datetime.now()

    return ret

def get_schedule_timestamp(frequency, startDate, endDate=None):
    ''' Returns a list of scheduled date from original date. '''

    if not endDate:
        endDate = startDate

    totalDays = (endDate - startDate).days

    multiplier = frequency == SC_ONCE and 1 or (totalDays / MULTIPLIER[frequency]) + 1

    days = []

    for i in range(multiplier):
        # Convert to timestamps
        dtstamp = timestamp_from_datetime(startDate)
        days.append(dtstamp)

        if frequency == SC_MONTHLY:
            nextMonth = startDate.month % 12 + 1
            nextMonthYear = startDate.year + ((startDate.month) / 12)
            startDate = datetime.datetime(nextMonthYear, nextMonth, startDate.day)
        else:
            delta = datetime.timedelta(days=MULTIPLIER[frequency])
            startDate = startDate + delta

    return days

def first_of_month(month, year):
    ''' Return the timestamp for the first day of the given month. '''
    ret = datetime.datetime(year, month, 1, 0, 0, 0)

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def last_of_month(month, year):
    ''' Return the timestamp for the last day of the given month. '''
    nextMonth = month % 12 + 1
    nextMonthYear = year + ((month) / 12)
    goback = datetime.timedelta(seconds=1)
    # Create datetime object with a timestamp corresponding the end of day
    nextMonth = datetime.datetime(nextMonthYear, nextMonth, 1, 0, 0, 0)
    ret = nextMonth - goback

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret

def get_alarm_timestamp(alertDays, alertTime, origDate):
    ''' Calculate alarm timestamp. '''

    if isinstance(origDate, float) or isinstance(origDate, int):
        origDate = datetime_from_timestamp(origDate)

    alertTime = alertTime.split(':')
    delta = datetime.timedelta(days=alertDays)
    alertDate = origDate - delta

    ret = datetime.datetime(alertDate.year, alertDate.month, alertDate.day, int(alertTime[0]), int(alertTime[1]))

    # Convert to timestamp
    ret = timestamp_from_datetime(ret)

    return ret
