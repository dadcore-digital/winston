import asyncio
from datetime import datetime
import io
import pytz
import sys
from random import randint, choice
import re
from pyquery import PyQuery as pq
import discord
import requests
from discord import Embed
from discord.ext import commands
from services.settings import get_settings
from services import db
from .services import Twitch
from .models import Stream

class Streaming(commands.Cog):

    def __init__(self, bot):
        pass
    
    @commands.command()
    async def streams(self, context, *args):
        """
        Show a list of all live Twitch streams for game.
        """
        await db.open()
        twitch = Twitch()
        streams = twitch.get_live_streams(simulate=True)

        prev_streams = await Stream.all().values_list(
            'twitch_id', flat=True)

        new_streams = []
        for stream in streams:
            if int(stream['id']) not in prev_streams:
                new_stream = await Stream.create(
                    twitch_id = stream['id'],
                    user_id = stream['user_id'],
                    user_name = stream['user_name'],
                    title = stream['title'],
                    viewer_count = stream['viewer_count'],
                    started_at = stream['started_at'],
                    thumbnail_url = stream['thumbnail_url']
                )
                new_streams.append(new_stream)
        
        if new_streams:            
            for stream in new_streams:

                # Sanity check before announcing
                now = datetime.utcnow().replace(tzinfo=pytz.utc)
                started_minutes_ago = (now - stream.started_at).seconds / 60
                embeds = []
                
                if started_minutes_ago <= 10:
                    link = f'https://twitch.tv/{stream.user_name}'
                    import ipdb; ipdb.set_trace() 
                    embed = Embed(
                        title=stream.title, color=0x009051, url=link)
                    embed.add_field(name='Streamer', value=stream.user_name, inline=True)
                    embed.add_field(name='Watching', value=stream.viewer_count, inline=True)
                    embed.add_field(name='Started At', value=stream.started_at, inline=False)
                    
                    thumbnail = stream.thumbnail_url.replace('{width}', '').replace('{height}', '')
                    embed.set_thumbnail(url=thumbnail)
                    msg = f'*{stream.user_name}* just went live!'
                    await contex.send(msg, embed=embed)
                
        msg = 'Dreadfully sorry, no streams currenty live.'
        await context.send(msg)
        await db.close()

