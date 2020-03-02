import re
import requests
from pyquery import PyQuery as pq
from discord import Embed
from discord.ext import commands


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKI_BASE_URL = 'https://killerqueenblack.wiki'
        self.SEARCH_URL = f'{self.WIKI_BASE_URL}/_search/?q='
        self.TRUNCATE_AT = 250

    @commands.command()
    async def wiki(self, context, *args):
        msg = 'No wiki article found'
        embed = None
        query = '+'.join(args)
        search_url = self.SEARCH_URL + query

        resp = requests.get(search_url)
        doc = pq(resp.content)
        result_links = doc('.table-striped tr').find('a')

        if result_links:
            query_as_path = query.replace('+', '-')

            # Default to first search result, even though often wrong
            result_path = result_links[0].attrib['href']

            # Path-ify search query and see if it matches URL path of
            # any search result links, select this result instead.
            for link in result_links:
                if link.attrib:
                    if query_as_path in link.attrib['href']:
                        result_path = link.attrib['href']
                        break

            result_url = f'{self.WIKI_BASE_URL}{result_path}'
            resp = requests.get(result_url)
            doc = pq(resp.content)
            article = doc('.wiki-article')

            if article:
                article_title = doc('title').text().split('-')[0].strip()
                article_text = article[0].text_content().strip()
                article_text = re.sub(r'\n\n\n+', '', article_text)
                article_text = article_text[:self.TRUNCATE_AT]
                article_link = result_url

                if len(article_text) >= self.TRUNCATE_AT:
                    article_text += '...'

                embed = Embed(title=article_title, color=0x009051, url=article_link)
                embed.add_field(name='Summary', value=article_text, inline=False)


        if embed:
            await context.send(embed=embed)
        else:
            await context.send(msg)
