from datetime import datetime
from random import choice
import arrow
import requests
from discord.ext import commands, tasks
from services.settings import get_settings
from services.events import get_matches_timeline, get_match_embed_dict

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

    @commands.command()
    async def matches(self, context, *args):
        """
        Show all matches in next 24 hours. Try `matches next` to see just next upcoming match.
        """
        timeline = get_matches_timeline()
        msg = '__Here are the matches for the next 24 hours:__'

        matches = []
        for entry in timeline:
            matches.append(get_match_embed_dict(entry))

        # Only Show next upcoming match if 'next' argument passed
        if 'next' in args:
            just_next_matches = []
            
            for idx, match in enumerate(matches):
                if idx == 0:
                    just_next_matches.append(match)
                else:
                    if match['begin_time'] == matches[0]['begin_time']:
                        just_next_matches.append(match)

            matches = just_next_matches

            if len(matches) == 1: 
                msg = '__Here is next upcoming match:__'
            else:
                msg = '__Here are the next upcoming matches (double-booked):__'
            
        
        await context.send(msg)

        for match in matches:
            await context.send(embed=match['embed'])
    
    @tasks.loop(seconds=60.0)
    async def announce(self):
        try:
            print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] Checking for upcoming matches...')

            raise ValueError('BLah')
            now = arrow.now()
            channel = self.bot.get_channel(self.CHANNEL_ID) 
        
            timeline = get_matches_timeline(end=240)
            matches = []
            for entry in timeline:
                minutes_until = (entry.begin - arrow.now()).seconds / 60 
                if (
                    minutes_until >= float(self.MINS_BEFORE)
                    and minutes_until <= float(self.MINS_BEFORE) + 1
                ):
                    matches.append(get_match_embed_dict(entry))

            if len(matches):
                print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {len(matches)} found.')
                plural = 'es' if len(matches) > 1 else ''  
                flavor = f'{choice(self.APOLOGY)}, {choice(self.HYPE)}!' 
                msg = f'{flavor}\n:loudspeaker:  __Match{plural} happening in {self.MINS_BEFORE} Minutes!__'
                await channel.send(msg)

                for match in matches:
                    await channel.send(embed=match['embed'])
            else:
                print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] No Upcoming Matches')

        except Exception as error:
            print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] ERROR: {error}')

    @announce.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()

