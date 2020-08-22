import discord
import re
import typing
from discord.ext import commands
from services.settings import get_settings
from .menus import get_pins_menu_pages


class Core(commands.Cog):
    def __init__(self, bot):
        settings = get_settings(['COGS', 'CORE'])

    @commands.command()
    async def pins(
        self, context, channel: typing.Optional[discord.TextChannel] = None,
        *args):
        """
        Show a pin. !pins, !pins #channel, !pins <search terms>, !pins #channel <search terms>
        """
        # Default: Get pins for current channel
        if channel:
            if context.author in channel.members:
                pins = await channel.pins()
            else:
                msg = 'Oh dear, you don\'t seem to have access to that channel. '
                await context.send(msg)
                return None
        else:
            pins = await context.channel.pins()
        
        if args:
            pin_search_results = []
            for pin in pins:

                found_content_match = False
                found_embed_match = False

                # Examine message content
                results = [x.lower() for x in args if x in pin.content.lower()]
                if len(args) == len(results):
                    found_content_match = True
                
                # Examine embed content
                embed_mega_text_blob = ''
                for embed in pin.embeds:
                    for field in embed.fields:
                        embed_mega_text_blob += f' {field.value}'
                
                results = [x.lower() for x in args if x in embed_mega_text_blob.lower()]
                if len(args) == len(results):
                    found_embed_match = True

                if found_content_match or found_embed_match:
                    pin_search_results.append(pin)

            pins = pin_search_results
                        
        if pins:
            pages = get_pins_menu_pages(pins)    
            await pages.start(context)
        else:
            msg = 'Quite embaressing I\'m afraid, no matching pins found.'
            await context.send(msg)



