import json
import os
from discord.ext import commands
from cogs.diagnostics import Diagnostic


# Private Key Settings: (Store all sensitive keys/other data for settings
# files outside version control)
cwd = os.path.dirname(os.path.realpath(__file__))
with open('%s/secrets.json' % cwd) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """
    Get secret variable or return explicit exception.

    Always return as string, not unicode.

    Must store this in base settings file due to structure of multiple
    settings files, or risk circular imports.
    """
    try:
        return str(secrets[setting])

    except KeyError:
        error_msg = "Missing %s setting from secrets file" % setting
        raise Exception(error_msg)


BOT_TOKEN = get_secret('BOT_TOKEN')
bot = commands.Bot(command_prefix=commands.when_mentioned)

bot.add_cog(Diagnostic(bot))

bot.run(BOT_TOKEN)
