import uuid
import io
import requests
from random import choice
from PIL import Image
from pyquery import PyQuery as pq
import discord
from discord.ext import commands
from tabulate import tabulate
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
        Automatic replies, added by mods. !show list to see all.
        """
        await db.open()
        try:
            responses = await Response.filter(shortcut=args[0])
            response = choice(responses)
            await context.send(response.text)
        
        except DoesNotExist:
            pass

        await db.close()

    @show.command()
    @commands.has_any_role(*ROLES_CAN_EDIT)
    async def add(self, context, *args):
        """
        [MODS ONLY] Add response: show add popranked "It's time to pop ranked!"
        """
        await db.open()
        shortcut = args[0]
        text = ' '.join(args[1:])
        response = Response(shortcut=shortcut, text=text)
        await response.save()
        await context.send(f'Added response `{shortcut} {text}`')
        await db.close()
        

    @show.command()
    @commands.has_any_role(*ROLES_CAN_EDIT)
    async def delete(self, context, *args):
        """
        [MODS ONLY] Delete an autoresponder: show delete popranked
        """
        await db.open()
        shortcut = args[0]

        try:
            responses = await Response.filter(shortcut=shortcut).order_by('id')

            if len(responses) == 1:
                await responses[0].delete()
                await context.send(f'`{shortcut}` **deleted.**')
            elif len(responses) > 1:
                if len(args) == 1:
                    headers = ['Index', 'Shortcut', 'Response']
                    table = []
                    for idx, response in enumerate(responses):
                        text = response.text
                        text = text.replace ('\n', ' ')

                        if len(text) > 50:
                            text = text[:49] + '...'
                        table.append([idx, response.shortcut, text]) 

                    table_data = tabulate(table, headers=headers, tablefmt='presto')
                    msg = f'__Here is a list of all auto-responders with that shorcut__:\n```\n{table_data}\n```'                
                    msg += f'Enter `show delete {shortcut} <index>` to delete a response.'
                    await context.send(msg)
                if len(args) == 2:
                    try:
                        index = int(args[1])
                        response = responses[index]
                        await response.delete()
                        await context.send(f'`{shortcut}[{index}]` **deleted.**')
                    except (IndexError, ValueError):
                        pass

        except DoesNotExist:
            pass

        await db.close()

    @show.command()
    async def list(self, context, *args):
        """
        List all auto responders available for use. 'list mobile' and 'list full' work too.
        """
        await db.open()
        responses = await Response.all()
        msg = '__Here all autoresponders__'
        headers = ['Shortcut', 'Response']
        tablefmt = 'presto'
        table = []

        # Accomodate different screen sizes on request.
        width = 50

        if args:
            if args[0] == 'mobile':
                width = 15
                tablefmt = 'simple'
            elif args[0] == 'full':
                width = 1024
                tablefmt = 'simple'

        for response in responses:
            text = response.text
            text = text.replace ('\n', ' ')

            if len(text) > width:
                text = text[:width-1] + '...'
            table.append([response.shortcut, text]) 

        table_data = tabulate(table, headers=headers, tablefmt=tablefmt)
        msg = f'__Here is a list of all auto-responders__:\n```\n{table_data}\n```'
        await context.send(msg)
        await db.close()


    @commands.command()
    async def bracket(self, context, *args):
        """
        Latest bracket by Tier. e.g."!bracket 2E", just "!bracket" for a list. 
        """
        width = 1400

        if args:

            bracket_name = args[0].upper()
            spreadsheet = settings['BRACKETS'][bracket_name]

            msg = f'Trying to retrieve bracket **{bracket_name}**. I beg your patience, it may take a moment or two.'
            await context.send(msg)

            url = f'https://image.thum.io/get/width/{width}/viewportWidth/{width}/png/{spreadsheet}'
            
            # Append random to bust cache
            url += f'?random={uuid.uuid4().hex}'

            response = requests.get(url)

            image = Image.open(io.BytesIO(response.content))
            top = 175
            bottom = 680
            left = 50
            right = 1380

            image = image.crop((left, top, right, bottom)) 

            image_as_buffer = io.BytesIO()

            image.save(image_as_buffer, format='PNG')
            image_as_buffer.seek(0)

            # file = discord.File(image_as_buffer, filename=f'bracket-{bracket_name}.png')
            # embed = discord.Embed()
            # embed.set_image(url=f'attachment://bracket-{bracket_name}.png', width=900)
            # await context.send(file=file, embed=embed)            
            
            await context.send(
                file=discord.File(image_as_buffer, f'bracket-{bracket_name}.png'))

        else:
            commands = ''
            
            for key in settings['BRACKETS']:
                commands += f' `!bracket {key}`,'

            commands = commands.rstrip(',')

            msg = f'Ah yes, try one of the following: {commands}.'
            await context.send(msg)
