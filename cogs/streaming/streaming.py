import aiohttp
import asyncio
from datetime import datetime
import io
import logging
import pytz
import sys
from random import randint, choice
import re
from pyquery import PyQuery as pq
import discord
import requests
from discord import Embed
from discord.ext import commands, tasks
from services.settings import get_settings
from services import db
from services.buzz import Buzz
from .services import get_stream_embed
from .menus import get_streams_menu_pages
from .models import Stream

class Streaming(commands.Cog):

    def __init__(self, bot):

        settings = get_settings(['COGS', 'STREAMING'])
        self.EXCLUDED_STREAMERS = settings['EXCLUDED_STREAMERS']
        self.CHANNEL_ID = settings['ANNOUNCE_WENT_LIVE_CHANNEL_ID']

        self.ENABLE_ANNOUNCE_TASK = settings['ENABLE_ANNOUNCE_TASK']
        
        if self.ENABLE_ANNOUNCE_TASK:
            self.announce.start()
        
        self.bot = bot

    def cog_unload(self):
        if self.ENABLE_ANNOUNCE_TASK:
            self.announce.cancel()

    @commands.command()
    async def streams(self, context, *args):
        """
        Show a list of all live Twitch streams for game.
        """
        buzz = Buzz()
        url = buzz.streams('is_live=true&blessed=true')

        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                streams = resp['results']

                if streams:
                    await context.send('__Here are all the live Twitch Streams for Killer Queen Black:__')
                    pages = get_streams_menu_pages(streams)    
                    await pages.start(context)

                else:
                    msg = 'Dreadfully sorry, no streams currenty live.'
                    await context.send(msg)

    @tasks.loop(seconds=10)
    async def announce(self):
        """
        Show a list of all live Twitch streams for game.
        """
        logging.info(f'[STREAMING] Checking for new Twitch streams...')
        try:
            await db.open()
            channel = self.bot.get_channel(self.CHANNEL_ID) 

            twitch = Twitch()
            streams = twitch.get_live_streams()

            prev_streams = await Stream.all().values_list(
                'twitch_id', flat=True)

            new_streams = []
            logging.info(f'[STREAMING] Found {len(new_streams)} new streams.')
            
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

            # Filter out banned streams
            blessed_new_streams = []
            for stream in new_streams:
                if stream.user_name not in self.EXCLUDED_STREAMERS:
                    blessed_new_streams.append(stream)        
            
            for stream in blessed_new_streams:

                # Sanity check before announcing
                now = datetime.utcnow().replace(tzinfo=pytz.utc)
                started_minutes_ago = (now - stream.started_at).seconds / 60
                embeds = []
                
                if started_minutes_ago <= 5:
                    embed = get_stream_embed({
                        'user_name': stream.user_name,
                        'title': stream.title,
                        'viewer_count': stream.viewer_count,
                        'started_at': stream.started_at,
                        'thumbnail_url': stream.thumbnail_url,
                    },
                        view_count=False
                    )

                    msg = f'**{stream.user_name}** just went live!'
                    await channel.send(msg, embed=embed)

            await db.close()
        
        except Exception as error:
            logging.info(f'[STREAMING] !!! ERROR !!!: {error}')

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

