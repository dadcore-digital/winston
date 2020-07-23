from datetime import datetime, timedelta
import pytz

def get_et_utc_offset():
    """Get Eastern Time UTC offset, taking into account daylight savings."""
    tz = pytz.timezone('US/Eastern')
    now = pytz.utc.localize(datetime.utcnow())
    is_edt = now.astimezone(tz).dst() != timedelta(0)

    if is_edt:
        return 4
    else:
        return 5
