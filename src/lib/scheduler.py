# -*- coding: utf-8 -*-

import calendar
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

def get_schedule_date(frequency, startDate, endDate=None):
    ''' Returns a list of scheduled date from original date. '''

    start = startDate
    # Takes care of endDates in the past
    if not endDate or endDate < start:
        endDate = start

    totalDays = (endDate - start).days

    multiplier = frequency == SC_ONCE and 1 or (totalDays / MULTIPLIER[frequency]) + 1

    days = []

    for i in range(multiplier):
        days.append(start)

        if frequency == SC_MONTHLY:
            nextMonth = start.month % 12 + 1
            nextMonthYear = start.year + ((start.month) / 12)
            # Check if we can use the same day of the month
            last_day = calendar.monthrange(nextMonthYear, nextMonth)[1]
            if startDate.day < last_day:
                last_day = startDate.day
            start = datetime.date(nextMonthYear, nextMonth, last_day)
        else:
            delta = datetime.timedelta(days=MULTIPLIER[frequency])
            start = start + delta

    return days

def first_of_month(month, year):
    ''' Return the timestamp for the first day of the given month. '''
    ret = datetime.date(year, month, 1)

    return ret

def last_of_month(month, year):
    ''' Return the timestamp for the last day of the given month. '''
    last_day = calendar.monthrange(month, year)[1]

    return datetime.date(year, month, last_day)

def get_alarm_timestamp(alertDays, alertTime, origDate):
    ''' Calculate alarm timestamp. '''

    if isinstance(origDate, float) or isinstance(origDate, int):
        origDate = datetime_from_timestamp(origDate)

    alertTime = alertTime.split(':')
    delta = datetime.timedelta(days=alertDays)
    alertDate = origDate - delta

    ret = datetime.datetime(alertDate.year, alertDate.month, alertDate.day, int(alertTime[0]), int(alertTime[1]))

    return ret

if __name__ == "__main__":
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    ninedaysahead = today + datetime.timedelta(days=9)
    nextweek = today + datetime.timedelta(weeks=1)
    next3weeks = today + datetime.timedelta(weeks=3)
    nextmonth = today + datetime.timedelta(days=30)
    next3months = today + datetime.timedelta(days=90)
    nextyear = today + datetime.timedelta(days=365)

    # Tests for non-repeatable tasks
    print "Repeat once, starting today, ending yesterday"
    repeats = get_schedule_date(SC_ONCE, today, yesterday)
    assert len(repeats) == 1, "Should have gotten one result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(today), "The date is wrong"

    print "Repeat once, starting today, ending nextweek"
    repeats = get_schedule_date(SC_ONCE, today, nextweek)
    assert len(repeats) == 1, "Should have gotten one result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(today), "The date is wrong"

    print "Repeat once, starting yesterday, ending today"
    repeats = get_schedule_date(SC_ONCE, yesterday, today)
    assert len(repeats) == 1, "Should have gotten one result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(yesterday), "The date is wrong"

    print "Repeat once, starting nextyear, ending today"
    repeats = get_schedule_date(SC_ONCE, nextyear, today)
    assert len(repeats) == 1, "Should have gotten one result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(nextyear), "The date is wrong"

    # Tests for weekly tasks
    print "Repeat weekly, starting today, ending yesterday"
    repeats = get_schedule_date(SC_WEEKLY, today, yesterday)
    assert len(repeats) == 1, "Should have gotten one result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(today), "The date is wrong"

    print "Repeat weekly, starting today, ending 9 days ahead"
    repeats = get_schedule_date(SC_WEEKLY, today, ninedaysahead)
    assert len(repeats) == 2, "Should have gotten 2 result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(today), "The date is wrong"

    print "Repeat weekly, starting today, ending 3 weeks ahead"
    repeats = get_schedule_date(SC_WEEKLY, today, next3weeks)
    assert len(repeats) == 4, "Should have gotten four result back! Got %s" % len(repeats)
    assert repeats[0] == timestamp_from_datetime(today), "The date is wrong"

