import json
import os
from discord.ext import commands
from cogs.diagnostics import Diagnostic
from utils.secrets import get_secret

# Secrets file location
cwd = os.path.dirname(os.path.realpath(__file__))
with open('%s/secrets.json' % cwd) as f:
    secrets_file = json.loads(f.read())

BOT_TOKEN = get_secret('BOT_TOKEN', secrets_file)
bot = commands.Bot(command_prefix=commands.when_mentioned)

bot.add_cog(Diagnostic(bot))

bot.run(BOT_TOKEN)
