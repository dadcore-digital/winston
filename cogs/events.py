import arrow
import requests
from discord.ext import commands
from ics import Calendar
from utils.secrets import get_secret


class Events(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.command()
    async def matches(self, context, *args):
        """
        Show matches for the upcoming 7 days.

        To see just all of today's matches, try:

            matches today

        """

        calendar_url = get_secret('MATCH_CALENDAR_ICS')
        ics_data = requests.get(calendar_url).text
        self.cal = Calendar(imports=ics_data)

        today = arrow.utcnow().floor('hour')
        seven_days_from_now = arrow.utcnow().shift(days=7).ceil('hour')

        timeline = self.cal.timeline.included(today, seven_days_from_now)

        msg = '**Here are the matches for the next 7 days:**'

        if args:
            if args[0] == 'today':
                msg = '**Here are the matches for today:**'
                timeline = self.cal.timeline.today()

        for num, entry in enumerate(timeline):

            title = entry.name
            begin_time = entry.begin.to('US/Eastern').format('ddd MMM Do @ h:mmA')
            time_until = entry.begin.humanize()
            stream = None

            if entry.description:
                try:
                    stream = entry.description.split('[stream]')[1].split('\n')[0].strip()
                except IndexError:
                    pass

            if num == 0:
                msg += '\n'

            msg += (
                f'\n__{title}__\n'
                f'{begin_time} ET\n'
                f'*{time_until}*\n'
            )

            if stream:
                msg += f'<{stream}>'

        await context.send(content=msg)
