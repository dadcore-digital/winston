import random
import requests
from pyquery import PyQuery as pq
from discord.ext import commands
from tortoise.exceptions import DoesNotExist
from services import db
from services.settings import get_settings
from .models import Response


settings = get_settings(['COGS', 'AUTORESPONDER'])
ROLES_CAN_EDIT = settings['ROLES_CAN_EDIT']

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.WIKI_BASE_URL = 'https://killerqueenblack.wiki'
        self.RESPONSES_URL = f'{self.WIKI_BASE_URL}/community/discord/winston/'

    @commands.group(invoke_without_command=True)
    async def show(self, context, *args):
        """
        Automatic replies supplied by you at: https://killerqueenblack.wiki/community/discord/winston/
        """
        await db.open()
        try:
            response = await Response.get(shortcut=args[0])
            await context.send(response.text)
        
        except DoesNotExist:
            pass

        await db.close()

    @show.command()
    @commands.has_any_role(*ROLES_CAN_EDIT)
    async def add(self, context, *args):
        """
        Add an autoresponder: show add popranked "It's time to pop ranked!"
        """
        await db.open()
        shortcut = args[0]
        text = ' '.join(args[1:])
        response = Response(shortcut=shortcut, text=text)
        await response.save()
        await context.send(f'Added response `!{shortcut} {text}`')
        await db.close()
        

    @show.command()
    @commands.has_any_role(*ROLES_CAN_EDIT)
    async def delete(self, context, *args):
        """
        Delete an autoresponder: show delete popranked
        """
        await db.open()
        shortcut = args[1]

        try:
            response = await Response.get(shortcut=shortcut)
            await response.delete()                
            await context.send(f'`{shortcut}` **deleted.**')
        
        except DoesNotExist:
            pass

        await db.close()

    @show.command()
    async def list(self, context, *args):
        """
        List all auto responders available for use.
        """
        await db.open()
        responses = await Response.all()
        msg = '__Here all autoresponders__'
        for response in responses:
            msg += f'\n`{response.shortcut}`:       {response.text}'

        await context.send(msg)
        await db.close()

