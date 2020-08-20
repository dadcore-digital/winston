from copy import copy
from discord.ext import menus
from services.menus import PermissiveMenuPages
from .services import get_stream_embed

class StreamsListSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entry):
        offset = menu.current_page * self.per_page
        embed = get_stream_embed(entry)
        embed.title = f'{embed.title.strip()} ({menu.current_page + 1}/{self.get_max_pages()})' 
        return embed

def get_streams_menu_pages(streams):
    """
    Use our special "PermissiveStreamsPages" version of ListPageSource to paginate
    a list of streams.

    Arguments:
    streams -- A list of match dicts to be converted to embeds and paginated.
               (list)
    """    
    pages = PermissiveMenuPages(
        StreamsListSource(streams), clear_reactions_after=True)

    pages.remove_button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK SQUARE FOR STOP}\ufe0f')

    return pages
