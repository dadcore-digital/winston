from random import randint
import re
import requests
from pyquery import PyQuery as pq
import discord
from discord import Embed
from discord.ext import commands


class Dice(commands.Cog):

    @commands.command()
    async def roll(self, context, *args):
        """
        Roll a die and display result.
        """
        emoji = discord.utils.get(context.bot.guilds[0].emojis, name='d61')
        try:
            dice_quantity, dice_type = args[0].split('d')
            dice_type = int(dice_type)
            dice_quantity = int(dice_quantity)

        except ValueError:
            dice_quantity = 1

        rolls = []
        for roll_number in range(dice_quantity):
            rolls.append(
                randint(1, dice_type)
            )

        msg = ''
        for result in rolls:
            emoji = discord.utils.get(
                context.bot.guilds[0].emojis,
                name=f'd{dice_type}{result}'
            )
            msg += str(emoji)

        await context.send(msg)

        if dice_quantity > 1:
            total = f'\nTotal: **{sum(rolls)}**'
            await context.send(total)
