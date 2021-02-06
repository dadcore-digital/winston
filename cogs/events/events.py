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
    get_event_embed, get_upcoming_matches, get_match_embed, get_next_match)
from .menus import get_event_menu_pages, get_match_menu_pages
import logging

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
        url = buzz.matches('days=90&scheduled=true')

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

    @commands.cooldown(1.0, 0, commands.BucketType.channel)
    @matches.command()
    async def team(self, context, *args):
        """
        Show all upcoming matches for a team.
        """
        query = '+'.join(args)
        buzz = Buzz()
        url = buzz.matches(f'team={query}&league={buzz.LEAGUE}&season={buzz.SEASON}')

        # Better safe than sorry
        if args:

            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    resp = await r.json()
                    upcoming_matches = resp['results']
                
                    if upcoming_matches:
                        embeds = []
                        for match in upcoming_matches:
                            embeds.append(get_match_embed(match))

                        pages = get_match_menu_pages(embeds)
                        await pages.start(context)
                    
                    else:
                        msg = f'Awkward. Could not find any matches for team name _{" ".join(args)}_. Try changing your search?'
                        await context.send(msg)

        else:
            msg = f'Pray enter a team name to show matches for.'
            await context.send(msg)


    @tasks.loop(seconds=60.0)
    async def announce(self):
        try:
            logging.info(
                f'[EVENTS] Querying Buzz API events in the next {self.MINS_BEFORE} minutes')

            channel = self.bot.get_channel(self.CHANNEL_ID) 

            buzz = Buzz()
            url = buzz.matches('starts_in_minutes=5')

            async with aiohttp.ClientSession() as cs:
                async with cs.get(url) as r:
                    resp = await r.json()

                    matches = resp['results']

                    if len(matches):
                        logging.info(f'[EVENTS] {len(matches)} events found!')

                        plural = 'es' if len(matches) > 1 else ''  
                        flavor = f'{choice(self.APOLOGY)}, {choice(self.HYPE)}!' 
                        msg = f'{flavor}\n:loudspeaker:  __Match{plural} happening in {self.MINS_BEFORE} Minutes!__'
                        await channel.send(msg)

                        for match in matches:
                            await channel.send(embed=get_match_embed(match))
                    else:
                        logging.info(f'[EVENTS] 0 events found.')
        
        except Exception as error:
            logging.info(f'!!! ERROR !!!: {error}')

    @commands.group(invoke_without_command=True)
    async def events(self, context, *args):
        """
        Show all events in next 14 days, paginated.
        """
        buzz = Buzz()
        url = buzz.events('days=14')
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                events = resp['results']
                msg = '__Here are the events for the next 14 days:__'

                embeds = []
                for event in events:
                    embeds.append(get_event_embed(event))

                # Catch case where there are no matches:
                if len(embeds) == 0:
                    msg = ':sob: No events in the next 14 days :sob:'
                
                await context.send(msg)

                if embeds:
                    pages = get_event_menu_pages(embeds)
                    await pages.start(context)

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

