from copy import copy
from discord.ext import menus
from services.menus import PermissiveMenuPages

class MatchListSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entry):
        offset = menu.current_page * self.per_page
        embed = copy(entry)
        embed.title = f'{embed.title.strip()} ({menu.current_page + 1}/{self.get_max_pages()})' 
        return embed

def get_match_menu_pages(matches):
    """
    Use our special "PermissiveMenuPages" version of ListPageSource to paginate
    a list of matches.

    Arguments:
    matches -- A list of match dicts to be converted to embeds and paginated.
               (list)
    """    
    pages = PermissiveMenuPages(
        MatchListSource(matches), clear_reactions_after=True)

    pages.remove_button('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f')
    pages.remove_button('\N{BLACK SQUARE FOR STOP}\ufe0f')

    return pages
