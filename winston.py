#! /home/ianfitzpatrick/apps/winston_bot/env/bin/python
import importlib
from discord.ext import commands
from cogs.autoresponder import AutoResponder
from services.settings import get_settings

BOT_TOKEN = get_settings('BOT_TOKEN')
LOAD_COGS = get_settings('LOAD_COGS')

async def get_pre(bot, message):
    prefixes = ['!']

    if not message.guild:
        prefixes.append('')

    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_pre)

for cog in LOAD_COGS:
    class_name = cog
    module_name = f'cogs.{cog.lower()}'
    module = importlib.import_module(module_name)
    class_ = getattr(module, class_name)
    bot.add_cog(class_(bot))

bot.run(BOT_TOKEN)
