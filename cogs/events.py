import requests
from discord.ext import commands
from services.secrets import get_secret
from services.events import get_matches_timeline, get_match_embed_dict

class Events(commands.Cog):
    def __init__(self, bot):
        pass

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

