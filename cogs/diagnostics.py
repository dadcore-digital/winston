import random
from discord.ext import commands


class Diagnostics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, context, *args):
        await context.send(' '.join(args))

    @commands.command()
    async def what(self, context, *args):
        choices = [
            'Search your heart for the answer.',
            'IDFK!',
            'You tell me.',
            'What do you think?',
            'I honestly don\'t know.'
        ]
        msg = random.choice(choices)
        await context.send(msg)
