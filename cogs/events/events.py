from datetime import datetime
from random import choice
import arrow
import requests
from discord.ext import commands, tasks
from services.settings import get_settings
from .services import (
    get_matches_timeline, get_match_embed_dict, get_next_match)
import logging

class Events(commands.Cog):
    def __init__(self, bot):
        self.announce.start()
        self.bot = bot
        
        settings = get_settings(['COGS', 'EVENTS'])

        self.MINS_BEFORE = settings['ANNOUNCE_MATCH_MINS_BEFORE']
        self.CHANNEL_ID = settings['ANNOUNCE_MATCH_CHANNEL_ID']
        self.APOLOGY = settings['ANNOUNCE_APOLOGY']
        self.HYPE = settings['ANNOUNCE_HYPE']
    
    def cog_unload(self):
        self.announce.cancel()

    @commands.group(invoke_without_command=True)
    async def matches(self, context, *args):
        """
        Show all matches in next 24 hours.
        """
        timeline = get_matches_timeline()
        msg = '__Here are the matches for the next 24 hours:__'

        matches = []
        for entry in timeline:
            matches.append(get_match_embed_dict(entry))
        
        # Catch case where there are no matches:
        if len(matches) == 0:
            msg = ':sob: No matches in the next 24 hours :sob:'
        
        await context.send(msg)

        for match in matches:
            await context.send(embed=match['embed'])

    @matches.command()
    async def next(self, context, *args):
        """
        Show the very next match on the calendar.
        """
        matches = []
        next_matches = get_next_match()
        
        for match in next_matches:
            matches.append(
                get_match_embed_dict(match)
            )

        if len(matches) == 1: 
            msg = '__Here is next upcoming match:__'
        elif len(matches) > 1: 
            msg = '__Here are the next upcoming matches (double-booked):__'
        else: 
            msg = ':sob: No scheduled matches in the upcoming 3 months...seriously? :sob:'

        for match in matches:
            await context.send(embed=match['embed'])

    @tasks.loop(seconds=60.0)
    async def announce(self):
        try:
            now = arrow.now()            
            channel = self.bot.get_channel(self.CHANNEL_ID) 
        
            logging.info(f'[EVENTS] Downloading matches between \'{now.strftime("%Y-%m-%d %H:%M:%S")}\' and \'{now.shift(minutes=240).strftime("%Y-%m-%d %H:%M:%S")}\'')
            timeline = get_matches_timeline(end=240)

            matches = []

            begin_range = arrow.now().floor('minute').shift(minutes=5)
            end_range = begin_range.shift(minutes=1)
            logging.info(f'[EVENTS] Examining matches for start times between \'{begin_range.strftime("%Y-%m-%d %H:%M:%S")}\' and \'{end_range.strftime("%Y-%m-%d %H:%M:%S")}\'')

            for entry in timeline:

                logging.info(f'[EVENTS] Evaluating {entry.name} @ {entry.begin}')

                if entry.begin.is_between(begin_range, end_range, '[)'):
                    logging.info(f'[EVENTS] !!! IN RANGE !!!: {entry.name} @ {entry.begin}')
                    matches.append(get_match_embed_dict(entry))
                else:
                    logging.info(f'[EVENTS] NOT IN RANGE: {entry.name} @ {entry.begin}')

            if len(matches):
                plural = 'es' if len(matches) > 1 else ''  
                flavor = f'{choice(self.APOLOGY)}, {choice(self.HYPE)}!' 
                msg = f'{flavor}\n:loudspeaker:  __Match{plural} happening in {self.MINS_BEFORE} Minutes!__'
                await channel.send(msg)

                for match in matches:
                    await channel.send(embed=match['embed'])

        except Exception as error:
            logging.info(f'!!! ERROR !!!: {error}')

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

