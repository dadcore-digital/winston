import asyncio
import re
from discord.ext import menus
from discord.ext.menus import Last
from .services import build_result_embed

class ResultsListSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    def is_paginating(self):
        """Paginate even when only one entry, so you can pick an item."""
        return True
    
    async def format_page(self, menu, result):
        offset = menu.current_page * self.per_page
        msg = f'__**Select a wiki search result [{menu.current_page + 1}/{self.get_max_pages()}]:**__\n\n'

        embed = build_result_embed(result)

        return {'content': msg, 'embed': embed}

class ResultsMenuPages(menus.MenuPages):

    def __init__(self, source, **kwargs):
        self._source = source
        self.current_page = 0
        super().__init__(source, timeout=None, **kwargs)

    @menus.button('\N{WHITE HEAVY CHECK MARK}', position=Last(1))
    async def on_select_pin(self, payload):
        selected_result = self.source.entries[self.current_page]

        embed = build_result_embed(selected_result)

        await self.message.edit(content='', embed=embed)
        await self.message.clear_reactions()
        self.stop()

    @menus.button('\N{NO ENTRY SIGN}', position=Last(0))
    async def on_cancel(self, payload):
        await self.message.delete()
        self.stop()

def get_results_menu_pages(results):
    """
    Get a list of all pins paginated.

    Arguments:
    pins -- A list pin messages. (list)
    """
    pages = ResultsMenuPages(
        ResultsListSource(results), clear_reactions_after=True)

    pages.remove_button('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK SQUARE FOR STOP}\ufe0f')
    return pages
