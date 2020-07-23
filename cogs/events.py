import arrow
import requests
from pyquery import PyQuery as pq
from discord import Embed
from discord.ext import commands
from ics import Calendar
from services.secrets import get_secret


class Events(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.command()
    async def matches(self, context, *args):
        """
        Show all matches in next 24 hours. Try `matches next` to see just next upcoming match.
        """

        calendar_url = get_secret('MATCH_CALENDAR_ICS')
        ics_data = requests.get(calendar_url).text
        self.cal = Calendar(imports=ics_data)

        now = arrow.utcnow()
        this_time_tomorrow = now.shift(hours=24)

        msg = '__Here are the matches for the next 24 hours:__'

        timeline = self.cal.timeline.included(
            now, this_time_tomorrow)

        embeds = []
        for entry in timeline:

            title = entry.name
            title = title.ljust(200 - len(title), ' ')
            title += '\n'
            begin_time = entry.begin.to('US/Eastern').format(
                'ddd MMM Do @ h:mmA')
            time_until = entry.begin.humanize()
            stream = 'TBD'

            embed = Embed(title=title, color=0x874efe)
            embed.add_field(name='Time', value=f'{begin_time} ET')
            embed.add_field(name='Countdown', value=time_until)

            if entry.description:

                # Handle inconsistent line breaks and split into list
                description = entry.description.replace('<br>', '\n')
                # description = entry.description.split('\n')

                embed.add_field(name='Details', value=description, inline=False)

            embeds.append(embed)


        # Only Show next upcoming match if 'next' argument passed
        if 'next' in args:
            embeds = embeds[:1]
            msg = '__Here is next upcoming match:__'

        await context.send(msg)

        for embed in embeds:
            await context.send(embed=embed)
