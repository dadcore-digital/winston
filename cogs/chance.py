import asyncio
import io
import sys
from random import randint, choice
import re
from pyquery import PyQuery as pq
import discord
from discord import Embed
from discord.ext import commands
from services.chance import (
    build_dice_roll_image, get_coin_flip_image, answer_flip_question)
from services.settings import get_settings

class Chance(commands.Cog):

    def __init__(self, bot):
        settings = get_settings(['COGS', 'CHANCE'])
        self.SIDES = settings['SIDES']
        self.INVALID_DICE_MESSAGES = settings['INVALID_DICE_MESSAGES']
        self.EXCESSIVE_ROLL_MESSAGES = settings['EXCESSIVE_ROLL_MESSAGES']
        self.INVALID_SIDE_ERRORS = settings['INVALID_SIDE_ERRORS']
        self.VALID_DICE_TYPES = settings['VALID_DICE_TYPES']
        self.FLIP_WIN = settings['FLIP_WIN']
        self.FLIP_LOSE = settings['FLIP_LOSE']
    
    @commands.command()
    async def roll(self, context, *args):
        """
        Roll some dice! Try: !roll d20, or !roll 2d6 5d8 4d20 3d12
        """

        msg = ''
        total = 0
        rolls = []
        
        valid_dice_types = [4, 6, 8, 10, 12, 20, 100, 1000]

        for arg in args:
            try:
                dice_quantity, dice_type = arg.split('d')
                dice_type = int(dice_type)
            
                if dice_type not in valid_dice_types:
                    await context.send(choice(self.INVALID_DICE_MESSAGES))
                    return None

                dice_quantity = int(dice_quantity)



            except ValueError:
                dice_quantity = 1

            for roll_number in range(dice_quantity):
                result = randint(1, dice_type)
                total += result
                rolls.append(f'd{dice_type}_{result}') 

        # Let's be reasonable.        
        if len(rolls) > 100:
            await context.send(choice(self.EXCESSIVE_ROLL_MESSAGES))
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

    @commands.command()
    async def flip(self, context, *, arg):
        """
        Flip a coin. Two choices: !flip heads OR !flip snails. 
        """
        result = choice(self.SIDES)
        call = ''
        params = arg.split(' ')
        # Weed out naughty flips
        if params:
            call = params[0]
            if call not in self.SIDES:
                await context.send(choice(self.INVALID_SIDE_ERRORS))
                return None

        msg = ''
        
        # Check for question argument 
        if len(params) > 1:
            msg = answer_flip_question(call, result, params[1:])

        elif call:
            if call == result:
                msg = f"{self.FLIP_WIN} **{result}**."
            else:
                msg = f"{self.FLIP_LOSE} **{result}**."

        image = get_coin_flip_image(result)
        await context.send(file=discord.File(image, 'flip.gif'))
        if msg:
            await asyncio.sleep(4)
            await context.send(msg)