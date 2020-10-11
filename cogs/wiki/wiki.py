import re
import requests
from pyquery import PyQuery as pq
from discord import Embed
from discord.ext import commands
from .menus import get_results_menu_pages


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKI_BASE_URL = 'https://killerqueenblack.wiki'
        self.SEARCH_URL = f'{self.WIKI_BASE_URL}/_search/?q='
        self.TRUNCATE_AT = 500

    @commands.command()
    async def wiki(self, context, *args):
        """
        Enter the title of a wiki article to (hopefully?) excerpt it.
        """
        msg = 'No wiki article found'
        other_results = ''

        embed = None
        query = '+'.join(args)
        search_url = self.SEARCH_URL + query

        resp = requests.get(search_url, timeout=context.bot.REQUESTS_TIMEOUT)
        doc = pq(resp.content)
        result_links = doc('.table-striped tr').find('td > a')

        results = []
        for link in result_links:
            result_dict = {
                'title': link.text,
                'link': f'{self.WIKI_BASE_URL}{link.attrib["href"]}',
                'summary': link.getnext().text_content(),
                'path': link.attrib['href'],
            }
            
            query_as_path = query.replace('+', '-')
            top_result = query_as_path.lower() in result_dict['title'].lower()
            result_dict['is_top'] = query_as_path.lower() in result_dict['title'].lower()
            results.append(result_dict)

        if results:
            sorted_results = sorted(results, key = lambda i: not i['is_top']) 



            pages = get_results_menu_pages(results)    
            await pages.start(context)

        else:
            await context.send(msg)
