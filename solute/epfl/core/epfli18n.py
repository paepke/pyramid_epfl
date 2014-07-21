#* encoding: utf-8

import pytz, dateutil.parser, datetime

TIMEZONE_PROVIDER = None

def set_timezone_provider(config, provider):
    global TIMEZONE_PROVIDER
    TIMEZONE_PROVIDER = provider


def get_timezone(request):
    """ Gets the current time-zone (bound and called to request.epfl_timezone) """
    if not TIMEZONE_PROVIDER:
        name = "Europe/Berlin"
    else:
        name = TIMEZONE_PROVIDER(request)

    return pytz.timezone(name)



def format_isodate(request, isodate_str, format):
    """ Converts a iso-formatted string into another format (also a string) """
    if not isodate_str:
        return None
        
    dateobj = dateutil.parser.parse(isodate_str)
    if not dateobj.tzinfo:
        dateobj = pytz.utc.localize(dateobj)
    dateobj = dateobj.astimezone(request.epfl_timezone)
    return dateobj.strftime(format)


def convert_to_isodate(request, time_str, format):
    """ Converts a time string (formatted with format) without timezone-info
    into a valid UTC-Isodate.
    Currently seconds are forced to 00 
    """
    dateobj = datetime.datetime.strptime(time_str, format)
    dateobj = request.epfl_timezone.localize(dateobj)
    dateobj = dateobj.astimezone(pytz.utc)
    return datetime.datetime.strftime(dateobj, "%Y-%m-%dT%H:%M:00")
