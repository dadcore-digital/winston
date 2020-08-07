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

class Chance(commands.Cog):

    @commands.command()
    async def roll(self, context, *args):
        """
        Roll some dice! Try: !roll d20, or !roll 2d6 5d8 4d20 3d12
        """

        msg = ''
        total = 0
        rolls = []
        
        invalid_dice_messages = [
            "Terribly sorry, adventure to all the fantastic worlds you want, but your dice types must be of a non-fantasy nature.",
            "Invented dice are strictly frowned upon.",
            "Dice of the imagination are best left in that realm.",
            "Do not trifle with the dice god! Your dice are invalid. Good day!",
            "What non-euclidean are you trying to get me to roll? I am not a cthulhu.",
            "Nah, hard pass."
        ]
        
        valid_dice_types = [4, 6, 8, 10, 12, 20, 100, 1000]

        excessive_roll_messages = [
            "Pardon me, but if I may say, that is an excessive amount of dice rolls.",
            "I cannot permit a fireball of that magnitude.",
            "Your meta-gaming is getting out of hand, I cannot in good conscience execute this roll.",
            "I love your moxy, but no. Just no.",
            "NERP!",
        ]

        for arg in args:
            try:
                dice_quantity, dice_type = arg.split('d')
                dice_type = int(dice_type)
            
                if dice_type not in valid_dice_types:
                    await context.send(choice(invalid_dice_messages))
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
            await context.send(choice(excessive_roll_messages))
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
        sides = ['heads', 'snails']

        invalid_side_errors = [
            'I do not recognize the legitmacy of that call.',
            'Call a side. No, not that one.',
            'I love you, but you are making a mockery of the process!',
            'Respect the game, dawg.',
            'Oh so we can just MAKE UP sides now huh? DENIED.'
        ]

        result = choice(sides)
        call = ''
        params = arg.split(' ')
        # Weed out naughty flips
        if params:
            call = params[0]
            if call not in sides:
                if call == 'tails':
                    await context.send(f'This is terribly awkward, but I think you meant to say *snails*, perhaps?')
                    return None
                else:
                    await context.send(choice(invalid_side_errors))
                    return None

        msg = ''
        
        # Check for question argument 
        if len(params) > 1:
            msg = answer_flip_question(call, result, params[1:])

        elif call:
            if call == result:
                msg = f"Very good, it is indeed **{result}**."
            else:
                msg = f"Dreadfully sorry, but that's **{result}**."

        image = get_coin_flip_image(result)
        await context.send(file=discord.File(image, 'flip.gif'))
        if msg:
            await asyncio.sleep(4)
            await context.send(msg)