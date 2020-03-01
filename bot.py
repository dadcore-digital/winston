from discord.ext import commands
from cogs.events import Events
from utils.secrets import get_secret

BOT_TOKEN = get_secret('BOT_TOKEN')
bot = commands.Bot(command_prefix=commands.when_mentioned)

bot.add_cog(Events(bot))

bot.run(BOT_TOKEN)
