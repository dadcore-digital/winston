import aiohttp
import asyncio
from discord.ext import commands
from services.buzz import Buzz
from services.formatting import format_list_as_commas
from .services import get_player_summary_embed

class Players(commands.Cog):
    @commands.command()
    async def player(self, context, *args):
        """
        Learn more about a player community member. !player <player name>
        """
        player_name = args[0]
        
        # Handle player names with spaces, without requiring quotes
        if len(args) > 1:
             player_name = ' '.join(args) 

        buzz = Buzz()
        url = buzz.players(f'name={player_name}')        
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url) as r:
                resp = await r.json()
                players = resp['results']
                
                # Just naively return the first result for now
                if len(players):

                    player = None
                    name_list = []

                    if len(players) == 1:
                        player = players[0]

                    # If more than one result found, use the result that 
                    # *exactly* matches.
                    if len(players) > 1:
                        for entry in players:
                            name_list.append(entry['name'])
                            
                            if entry['name'] == player_name:
                                player = entry                                
                                break
                        
                        # No exact match found
                        if not player:
                            msg = f'Found multiple results for **{player_name}**. Pray try narrowing your search.\n\n'
                            msg += f'>>> **Results**\n*{format_list_as_commas(name_list[:8])}*'
                            await context.send(msg)

                    embed = get_player_summary_embed(player)
                    await context.send(embed=embed)

                else:
                    msg = 'Terribly dreadful, I could not find that player for you.'
                    await context.send(msg)
