import io
import sys
from random import randint
import re
from pyquery import PyQuery as pq
import discord
from discord import Embed
from discord.ext import commands
from services.dice import build_dice_roll_image

class Dice(commands.Cog):

    @commands.command()
    async def roll(self, context, *args):
        """
        Roll some dice! Try: !roll d20, or !roll 2d6 5d8 4d20 3d12
        """

        msg = ''
        total = 0
        rolls = []
        
        for arg in args:
            try:
                dice_quantity, dice_type = arg.split('d')
                dice_type = int(dice_type)
                dice_quantity = int(dice_quantity)

            except ValueError:
                dice_quantity = 1

            for roll_number in range(dice_quantity):
                result = randint(1, dice_type)
                total += result
                rolls.append(f'd{dice_type}_{result}') 

        # Let's be reasonable.        
        if len(rolls) > 100:
            return None

        # Avoid writing image to disk
        image = build_dice_roll_image(rolls)
        image_as_buffer = io.BytesIO()
        image.save(image_as_buffer, format='PNG')
        image_as_buffer.seek(0)

        await context.send(file=discord.File(image_as_buffer, 'roll.png'))

        if dice_quantity > 1 or len(args) > 1:
            total_msg = f'\nTotal: **{total}**'
            await context.send(total_msg)
