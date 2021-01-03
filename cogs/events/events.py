import aiohttp
import asyncio
from datetime import datetime
from random import choice
import arrow
import requests
from discord.ext import commands, tasks
from services.buzz import Buzz
from services.menus import PermissiveMenuPages
from services.settings import get_settings
from .services import (
    get_upcoming_matches, get_match_embed, get_next_match)
from .menus import get_match_menu_pages
import logging

from concurrent.futures import ProcessPoolExecutor

settings = get_settings(['COGS', 'EVENTS'])
MATCHES_COOLDOWN = settings['MATCHES_COOLDOWN']

class Events(commands.Cog):
    def __init__(self, bot):
        self.announce.start()
        self.bot = bot
        
        self.MINS_BEFORE = settings['ANNOUNCE_MATCH_MINS_BEFORE']
        self.CHANNEL_ID = settings['ANNOUNCE_MATCH_CHANNEL_ID']
        self.APOLOGY = settings['ANNOUNCE_APOLOGY']
        self.HYPE = settings['ANNOUNCE_HYPE']
    
    def cog_unload(self):
        self.announce.cancel()


    @commands.cooldown(1.0, MATCHES_COOLDOWN, commands.BucketType.channel)
    @commands.group(invoke_without_command=True)
    async def matches(self, context, *args):
        """
        Show all matches in next 24 hours, paginated.
        """
        buzz = Buzz()
        url = buzz.matches('hours=24')
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                matches = resp['results']
                msg = '__Here are the matches for the next 24 hours:__'

                embeds = []
                for match in matches:
                    embeds.append(get_match_embed(match))

                # Catch case where there are no matches:
                if len(embeds) == 0:
                    msg = ':sob: No matches in the next 24 hours :sob:'
                
                await context.send(msg)

                if embeds:
                    pages = get_match_menu_pages(embeds)
                    await pages.start(context)


    @matches.command()
    async def full(self, context, *args):
        """
        Show all matches in next 24 hours non-paginated.
        """
        buzz = Buzz()
        url = buzz.matches('hours=24')

        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                matches = resp['results']

                msg = '__Here are the matches for the next 24 hours:__'

                embeds = []
                for match in matches:
                    embeds.append(get_match_embed(match))

                # Catch case where there are no matches:
                if len(matches) == 0:
                    msg = ':sob: No matches in the next 24 hours :sob:'
                
                await context.send(msg)
                for embed in embeds:
                    await context.send(embed=embed)

    @matches.command()
    async def next(self, context, *args):
        """
        Show the very next match on the calendar.
        """
        buzz = Buzz()
        url = buzz.matches('days=90')

        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                upcoming_matches = resp['results']

                next_matches = get_next_match(upcoming_matches)

                embeds = []
                for match in next_matches:
                    embeds.append(get_match_embed(match))

                if len(embeds) == 1: 
                    msg = '__Here is next upcoming match:__'
                elif len(embeds) > 1: 
                    msg = '__Here are the next upcoming matches (double-booked):__'
                else: 
                    msg = ':sob: No scheduled matches in the upcoming 3 months...seriously? :sob:'

                await context.send(msg)

                if len(embeds) == 1:
                    await context.send(embed=embeds[0])
                
                elif len(embeds) > 1:
                    pages = get_match_menu_pages(embeds)
                    await pages.start(context)

    @tasks.loop(seconds=60.0)
    async def announce(self):
        try:
            logging.info(
                f'[EVENTS] Querying Buzz API events in the next {self.MINS_BEFORE} minutes')

            channel = self.bot.get_channel(self.CHANNEL_ID) 
            matches = get_upcoming_matches(minutes=self.MINS_BEFORE)


            if len(matches):
                logging.info(f'[EVENTS] {len(matches)} events found!')

                plural = 'es' if len(matches) > 1 else ''  
                flavor = f'{choice(self.APOLOGY)}, {choice(self.HYPE)}!' 
                msg = f'{flavor}\n:loudspeaker:  __Match{plural} happening in {self.MINS_BEFORE} Minutes!__'
                await channel.send(msg)

                for match in matches:
                    await channel.send(embed=get_match_embed(match)['embed'])
            else:
                logging.info(f'[EVENTS] 0 events found.')
        
        except Exception as error:
            logging.info(f'!!! ERROR !!!: {error}')

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

