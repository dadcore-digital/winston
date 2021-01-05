import arrow
import re
import requests
from discord import Embed
from services.settings import get_settings

def get_stream_embed(stream_dict, view_count=True):

    link = f'https://twitch.tv/{stream_dict["username"]}'
    embed = Embed(
        title=stream_dict['name'], color=0x009051, url=link)
    embed.add_field(name='Streamer', value=stream_dict['username'], inline=True)
    
    if view_count:
        embed.add_field(
            name='Peak Viewers',
            value=stream_dict['max_viewer_count'], inline=True
        )
    
    present = arrow.utcnow()
    start_time = arrow.get(stream_dict['start_time']) 
    went_live =start_time.humanize(present, granularity=["hour", "minute"])
    went_live = re.sub(r'^0 hours and ', '', went_live)

    embed.add_field(name='Went Live', value=went_live, inline=False)
    
    thumbnail = stream_dict['thumbnail'].replace('{width}', '').replace('{height}', '')
    embed.set_thumbnail(url=thumbnail)

    return embed
