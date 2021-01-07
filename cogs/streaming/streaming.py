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

    @tasks.loop(seconds=60)
    async def announce(self):
        """
        Show a list of all live Twitch streams for game.
        """
        MINS_BEFORE=0
        buzz = Buzz()
        url = buzz.streams(
            f'started_n_minutes_ago={MINS_BEFORE}&is_live=true&blessed=true')

        logging.info(
            f'[STREAMS] Querying Buzz API for streams that started 0 {MINS_BEFORE} minutes ago')

        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                streams = resp['results']

                channel = self.bot.get_channel(self.CHANNEL_ID) 

                logging.info(f'[STREAMS] {len(streams)} new live streams found!')

                for stream in streams:

                    embed = get_stream_embed({
                        'username': stream.user_name,
                        'name': stream.title,
                        'max_viewer_count': stream.viewer_count,
                        'start_time': stream.started_at,
                        'thumbnail': stream.thumbnail_url,
                    },
                        view_count=False
                    )

                    msg = f'**{stream.user_name}** just went live!'
                    await channel.send(msg, embed=embed)
        
    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

