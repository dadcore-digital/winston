import asyncio
import arrow
import re
from discord.ext import menus
from discord.ext.menus import Last
from services.time import trim_humanize

class PinsListSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    def is_paginating(self):
        """Paginate even when only one entry, so you can pick an item."""
        return True
    
    async def format_page(self, menu, entry):
        offset = menu.current_page * self.per_page
        msg = f'__**Select a pin to display [{menu.current_page + 1}/{self.get_max_pages()}]:**__\n\n'

        embed = None
        if entry.embeds:
            embed = entry.embeds[0]

        pin_created = arrow.get(entry.created_at).humanize(granularity=['day', 'hour', 'minute']) 
        pin_created = trim_humanize(pin_created)

        if entry.author.nick:
            msg += f'*by @{entry.author.nick} ({pin_created})*'
        else:
            msg += f'*{pin_created}*'

        msg += '\n\n'

        if entry.clean_content:
            msg += f'>>> '
            msg += entry.clean_content

        for attachment in entry.attachments:
            msg += f'\n{attachment.url}'

        return {'content': msg, 'embed': embed}

class PinsMenuPages(menus.MenuPages):

    def __init__(self, source, **kwargs):
        self._source = source
        self.current_page = 0
        super().__init__(source, timeout=None, **kwargs)

    @menus.button('\N{WHITE HEAVY CHECK MARK}', position=Last(0))
    async def on_select_pin(self, payload):
        selected_pin = self.source.entries[self.current_page]
        pin_created = arrow.get(selected_pin.created_at).humanize(granularity=['day', 'hour', 'minute']) 
        pin_created = f'[{trim_humanize(pin_created)}]'

        embed = None
        if selected_pin.embeds:
            embed = selected_pin.embeds[0]
        
        msg = f'**@{self.ctx.author.nick }** shared a pin:\n\n'

        pin_created = arrow.get(selected_pin.created_at).humanize(granularity=['day', 'hour', 'minute']) 
        pin_created = trim_humanize(pin_created)

        if selected_pin.author.nick:
            msg += f'*by @{selected_pin.author.nick} ({pin_created})*'
        else:
            msg += f'*{pin_created}*'

        msg += '\n\n'
        
        if selected_pin.content:
            msg += f'>>> {selected_pin.content}'

        for attachment in selected_pin.attachments:
            msg += f'\n{attachment.url}'

        await self.message.edit(content=msg, embed=embed)
        
        self.stop()

def get_pins_menu_pages(pins):
    """
    Get a list of all pins paginated.

    Arguments:
    pins -- A list pin messages. (list)
    """
    pages = PinsMenuPages(
        PinsListSource(pins), clear_reactions_after=True)

    pages.remove_button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    return pages
