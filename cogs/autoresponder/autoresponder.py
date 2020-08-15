import random
import requests
from pyquery import PyQuery as pq
from discord.ext import commands
from tortoise.exceptions import DoesNotExist
from .models import Response
from services import db

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.WIKI_BASE_URL = 'https://killerqueenblack.wiki'
        self.RESPONSES_URL = f'{self.WIKI_BASE_URL}/community/discord/winston/'

    @commands.command()
    async def show(self, context, *args):
        """
        Automatic replies supplied by you at: https://killerqueenblack.wiki/community/discord/winston/
        """
        await db.open()

        if args[0] == 'add':
            shortcut = args[1]
            text = args[2]
            response = Response(shortcut=shortcut, text=text)
            await response.save()
            await context.send(f'Added response `!{shortcut} {text}`')

        elif args[0] == 'list':
            responses = await Response.all()
            msg = '__Here all autoresponders__'
            for response in responses:
                msg += f'\n`{response.shortcut}`:       {response.text}'

            await context.send(msg)

        elif args[0] == 'remove' or args[0] == 'del':
            shortcut = args[1]
            try:
                response = await Response.get(shortcut=shortcut)
                await response.delete()                
                await context.send(f'`{shortcut}` **deleted.**')
            
            except DoesNotExist:
                pass


        else:
            try:
                response = await Response.get(shortcut=args[0])
                await context.send(response.text)
            
            except DoesNotExist:
                pass

        await db.close()
        
