import aiohttp
import asyncio
from discord.ext import commands
from services.buzz import Buzz
from .services import get_player_summary_embed

class Players(commands.Cog):
    @commands.command()
    async def player(self, context, *args):
        """
        Learn more about a player community member. !player <player name>
        """
        player_name = args[0]

        buzz = Buzz()
        url = buzz.players(f'name={player_name}')        
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                players = resp['results']
                
                # Just naively return the first result for now
                if len(players):
                    
                    embed = get_player_summary_embed(players[0])
                    await context.send(embed=embed)

                else:
                    msg = 'Terribly dreadful, I could not find that player for you.'
                    await context.send(msg)
