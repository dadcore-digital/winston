import aiohttp
import asyncio
from discord.ext import commands
from discord import Embed
from services.buzz import Buzz
from .services import get_steam_players


class Playing(commands.Cog):

    @commands.group(invoke_without_command=True)
    async def playing(self, context, *args):
        """
        See who is playing Killer Queen Black.
        """
        buzz = Buzz()
        url = buzz.playing()
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                playing = resp['results'][0]
                steam = get_steam_players(playing['total'])

                embed = Embed(title='Playing Killer Queen Black Now', color=0x874efe)    
                embed.add_field(
                    name='Steam', value=steam['count'], inline=True)

                await context.send(embed=embed)
