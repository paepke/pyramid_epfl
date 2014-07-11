#* encoding: utf-8

import pytz, dateutil.parser

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
    dateobj = dateutil.parser.parse(isodate_str)
    if not dateobj.tzinfo:
        dateobj = pytz.utc.localize(dateobj)
    dateobj = dateobj.astimezone(request.epfl_timezone)
    return dateobj.strftime(format)
