"""
Timezone Utility Functions
"""

from datetime import datetime
import pytz


def is_dst():
    """
    Determine whether or not Daylight Savings Time (DST)
    is currently in effect
    """

    # Jan 1 of the current year
    x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('US/Eastern'))

    y = datetime.now(pytz.timezone('US/Eastern'))

    # If DST is in effect, their offsets will be different
    return not (y.utcoffset() == x.utcoffset())