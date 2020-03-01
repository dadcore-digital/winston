from discord.ext import commands
from cogs.events import Events
from utils.secrets import get_secret

BOT_TOKEN = get_secret('BOT_TOKEN')

async def get_pre(bot, message):
    prefixes = ['!w ']

    if not message.guild:
        prefixes.append('')

    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_pre)

bot.add_cog(Events(bot))

bot.run(BOT_TOKEN)
