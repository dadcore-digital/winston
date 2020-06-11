from random import randint
import re
import requests
from pyquery import PyQuery as pq
from discord import Embed
from discord.ext import commands


class Dice(commands.Cog):

    def __init__(self, bot):
        self.d6 = [
            '<:d61:720736504745558056>',
            '<:d62:720737138391646370>',
            '<:d63:720737138294915104>',
            '<:d64:720737138672402452>',
            '<:d65:720737138613944340>',
            '<:d66:720737138706219128>'
        ]

    @commands.command()
    async def roll(self, context, *args):
        """
        Roll a die and display result.
        """

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
            msg += getattr(self, f'd{dice_type}')[result - 1]

        await context.send(msg)

        if dice_quantity > 1:
            total = f'\nTotal: **{sum(rolls)}**'
            await context.send(total)
