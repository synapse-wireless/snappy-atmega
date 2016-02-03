# (c) Copyright 2011-2016, Synapse Wireless, Inc.
"""ATmega128RFA1 clock/event alarm

Currently uses Timer5, but could be modified to use a different timer

Note: The time must be set using the set_time function

Ex.
  #Setup timer5 as a free running timer keeper
  @setHook(HOOK_STARTUP)
  def startup():
      timer_init(TMR5, WGM_FASTPWM16_TOP_ICR, CLK_FOSC_DIV1024, 0x3d09)

  @setHook(HOOK_100MS)
  def timer_100ms():
      clock_timer_100ms()
"""

from timers import *

# Define constant
MONTH = 0
DAY = 1
YEAR = 2
HOUR = 4
MINUTE = 5
SECOND = 6
DAYS_IN_MONTH = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# Global variables
START_TIME = "\x01\x01\x07\xD0\x18\x00\x00"
time_str = START_TIME
alarm_time = "\x00\x00\x00\x00\x00\x00\x00"
rtc_alarm = 0


def clock_timer_100ms():
    """This function needs to be hooked into the 100ms hook"""
    global lastTime
    cTime = get_tmr_count(TMR5) >> 8
    if cTime < lastTime:
        clock_tick()
    lastTime = cTime


def rtc_set_alarm(month, day, year, hour, minute, second):
    """Set the alarm time and date 0-24 hour"""
    global alarm_time
    alarm_time = chr(month) + chr(day) + chr(year >> 8) + chr(year & 0xFF) + chr(hour) + chr(minute) + chr(second)


def rtc_clear_alarm():
    global rtc_alarm
    rtc_alarm = 0


def check_alarms():
    """Check the time against the alarm time and call the event if match"""
    global rtc_alarm
    if time_str == alarm_time:
        rtc_alarm = 1


def rtc_set_time(month, day, year, hour, minute, second):
    """Set the current time and date 0-24 hour"""
    global time_str
    time_str = chr(month) + chr(day) + chr(year >> 8) + chr(year & 0xFF) + chr(hour) + chr(minute) + chr(second)

    # clear timers
    set_tmr_count(TMR5, 0)


def read_alarm():
    """Return the alarm time and date in printable ASCII"""
    return parse_time(alarm_time)


def read_time():
    """Return the current time and date in printable ASCII"""
    return parse_time(time_str)


def get_hours():
    """Return the current hours in printable ASCII"""
    time = time_str
    myStr = ''
    hour = ord(time[HOUR])
    if hour < 10:
        myStr += '0' + str(hour)
    else:
        myStr += str(hour)
    myStr += ':'

    minute = ord(time[MINUTE])
    if minute < 10:
        myStr += '0' + str(minute)
    else:
        myStr += str(minute)
    myStr += ':'

    second = ord(time[SECOND])
    if second < 10:
        myStr += '0' + str(second)
    else:
        myStr += str(second)
    return myStr


def get_date():
    """Convert the date string into printable ASCII"""
    time = time_str
    myStr = str(ord(time[MONTH])) + '/'
    myStr += str(ord(time[DAY])) + '/'
    year = ord(time[YEAR]) << 8 | ord(time[YEAR+1])
    myStr += str(year)
    return myStr


def parse_time(time):
    """Convert the time string into printable ASCII"""
    myStr = str(ord(time[MONTH])) + '/'
    myStr += str(ord(time[DAY])) + '/'
    year = ord(time[YEAR]) << 8 | ord(time[YEAR+1])
    myStr += str(year) + ' '

    hour = ord(time[HOUR])
    if hour < 10:
        myStr += '0' + str(hour)
    else:
        myStr += str(hour)
    myStr += ':'

    minute = ord(time[MINUTE])
    if minute < 10:
        myStr += '0' + str(minute)
    else:
        myStr += str(minute)
    myStr += ':'

    second = ord(time[SECOND])
    if second < 10:
        myStr += '0' + str(second)
    else:
        myStr += str(second)
    return myStr


def clock_tick():
    """This function is automatically called to increment the clock string"""
    global time_str

    # See if we have any impending alarms
    check_alarms()

    second = ord(time_str[SECOND])
    if second == 59:
        time_str = time_str[0:SECOND] + "\x00"
        minute = ord(time_str[MINUTE])
        if minute == 59:
            time_str = time_str[0:MINUTE] + "\x00" + time_str[SECOND]
            hour = ord(time_str[HOUR])
            if hour == 23:
                time_str = time_str[0:HOUR] + chr(24) + time_str[MINUTE:]
                month = ord(time_str[MONTH])
                day = ord(time_str[DAY])
                year = ord(time_str[YEAR]) << 8 | ord(time_str[YEAR+1])
                if day == get_days_in_month(month, year):
                    if month == 12:
                        year += 1
                        time_str = "\x01\x01" + chr(year >> 8) + chr(year & 0xFF) + time_str[HOUR:]
                    else:
                        month += 1
                        time_str = chr(month) + time_str[DAY:]
                else:
                    day += 1
                    time_str = time_str[0:DAY] + chr(day) + time_str[YEAR:]
            elif hour == 24:
                time_str = time_str[0:HOUR] + "\01" + time_str[MINUTE:]
            else:
                hour += 1
                time_str = time_str[0:HOUR] + chr(hour) + time_str[MINUTE:]
        else:
            minute += 1
            time_str = time_str[0:MINUTE] + chr(minute) + time_str[SECOND]
    else:
        second += 1
        time_str = time_str[0:SECOND] + chr(second)


def is_leap_year(year):
    """Determine whether the specified year is a leap year"""
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return 1
            else:
                return 0
        else:
            return 1
    else:
        return 0


def get_days_in_month(month, year):
    """Determine days in the month/year combination"""
    if month == 2:
        return DAYS_IN_MONTH[month] + is_leap_year(year)
    else:
        return DAYS_IN_MONTH[month]
