import random
import requests
from pyquery import PyQuery as pq
from discord.ext import commands


class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.WIKI_BASE_URL = 'https://killerqueenblack.wiki'
        self.RESPONSES_URL = f'{self.WIKI_BASE_URL}/community/discord/winston/'

    @commands.command()
    async def show(self, context, *args):
        """
        Automatic replies supplied by you at: https://killerqueenblack.wiki/community/discord/winston/
        """
        query = ' '.join(args)

        resp = requests.get(self.RESPONSES_URL)
        doc = pq(resp.content)
        article = doc('.wiki-article')
        msg = f'Shortcut to autoresponder is missing? Double check: <{self.RESPONSES_URL}>'

        shortcuts = article(':header')

        # Match all headers and extract following paragraph or link text value
        # as responder.
        for shortcut in shortcuts:
            if query.lower() in shortcut.text.lower():
                response_text = shortcut.getnext().text

                # Do acrobatics in order to extract anchor href value
                if not response_text:
                    child_anchors = shortcut.getnext().getchildren()
                    if child_anchors:
                        response_text = child_anchors[0].attrib['href']

                msg = response_text

        await context.send(msg)
