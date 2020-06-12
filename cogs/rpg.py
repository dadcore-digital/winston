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

        msg = ''
        total = 0

        for arg in args:
            try:
                dice_quantity, dice_type = arg.split('d')
                dice_type = int(dice_type)
                dice_quantity = int(dice_quantity)

            except ValueError:
                dice_quantity = 1

            rolls = []
            for roll_number in range(dice_quantity):
                result = randint(1, dice_type)
                total += result
                rolls.append(result)

            for result in rolls:
                emoji = discord.utils.get(
                    context.bot.guilds[0].emojis,
                    name=f'd{dice_type}_{result}'
                )
                msg += str(emoji)

        await context.send(msg)

        if dice_quantity > 1 or len(args) > 1:
            total_msg = f'\nTotal: **{total}**'
            await context.send(total_msg)
