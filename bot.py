import json
import os
import random
import discord
from discord.ext import commands

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
        raise ImproperlyConfigured(error_msg)


BOT_TOKEN = get_secret('BOT_TOKEN')
bot = commands.Bot(command_prefix=commands.when_mentioned)


@bot.command()
async def echo(context, *args):
    await context.send(' '.join(args))


@bot.command()
async def what(context, *args):
    choices = [
        'Search your heart for the answer.',
        'IDFK!',
        'You tell me.',
        'What do you think?',
        'I honestly don\'t know.'
    ]
    msg = random.choice(choices)
    await context.send(msg)


bot.run(BOT_TOKEN)
