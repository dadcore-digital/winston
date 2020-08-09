import re
import arrow
import requests
from .settings import get_settings
from ics import Calendar
from discord import Embed

def get_matches_timeline(start=0, end=1500):
    """
    Return a timeline of matches.

    Connect to the KQB Calendar and convert all calendar data
    to an Timeline generator.

    Keyword arguments:
    start -- Beginning of timeline in minutes, relative to now. 0 means now. (int)
    end -- End of timeline in minutes, relative to start. Default is 1500
           (24 + 1 hour for event length). (int)
    """
    settings = get_settings(['COGS', 'EVENTS'])
    calendar_url = settings['MATCH_CALENDAR_ICS']
    ics_data = requests.get(calendar_url).text
    cal = Calendar(imports=ics_data)
    start = arrow.utcnow().shift(minutes=start)
    end = start.shift(minutes=end)
    timeline = cal.timeline.included(start, end)
    
    return timeline

def get_match_embed_dict(entry):
    """
    Return dictionary of match times and discord embeds given timelie entry.

    Keyword arguments:
    entry -- An instance of event/entry (not sure proper word) in a Timeline
             generator.
    """
    title = entry.name
    title = title.ljust(200 - len(title), ' ')
    title += '\n'
    begin_time = entry.begin.to('US/Eastern').format(
        'ddd MMM Do @ h:mmA')
    time_until = entry.begin.humanize(granularity=['hour', 'minute'])
    stream = 'TBD'

    link = ''
    try:
        res = re.search('(https://twitch.tv/.*)\n', entry.description) 
        if res:
            link = res.groups()[0]  
    except:
        pass

    embed = Embed(title=title, color=0x874efe, url=link)
    embed.add_field(name='Time', value=f'{begin_time} ET')
    embed.add_field(name='Countdown', value=time_until)

    if entry.description:

        # Handle inconsistent line breaks and split into list
        description = entry.description.replace('<br>', '\n')

        embed.add_field(name='Details', value=description, inline=False)

    return {'begin_time': begin_time, 'embed': embed}