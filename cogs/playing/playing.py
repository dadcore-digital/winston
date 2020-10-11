from discord.ext import commands
from discord import Embed
from .services import get_steam_players


class Playing(commands.Cog):

    @commands.group(invoke_without_command=True)
    async def playing(self, context, *args):
        """
        See who is playing Killer Queen Black.
        """
        steam = get_steam_players()
        

        embed = Embed(title='Playing Killer Queen Black Now', color=0x874efe)    
        embed.add_field(
            name='Steam', value=steam['count'], inline=True)

        await context.send(embed=embed)

    @playing.command()
    async def steam(self, context, *args):
        """
        Get count of live Steam players in Killer Queen Black.
        """
        steam = get_steam_players()
        await context.send(steam['msg'])
        
    