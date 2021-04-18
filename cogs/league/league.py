import aiohttp
import asyncio
from discord.ext import commands
from discord import Embed
from services.buzz import Buzz


class League(commands.Cog):
    
    @commands.group(invoke_without_command=True)
    async def signups(self, context, *args):
        """
        See how many teams and players are signed up for BGL.
        """
        buzz = Buzz()
        url = f"{buzz.API_BASE}/circuits?is_active=true&format=json"
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                embed = Embed(title=':chart_with_upwards_trend: BGL Circuit Signups', color=0x874efe)
            
                for circuit in resp['results']:
                    circuit_name = f"{circuit['name']} {circuit['season']['name']}"
                    teams = len(circuit['teams'])
                    players = 0
                    for team in circuit['teams']:
                        players += len(team['members'])
                    embed.add_field(name=circuit_name, value=f'Teams: {teams}\nPlayers: {players}')
                await context.send(embed=embed)
