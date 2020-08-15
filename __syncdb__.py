import importlib
from tortoise import Tortoise, run_async
from services.settings import get_settings


async def init():
    DATABASE_PATH = get_settings('DATABASE_PATH')
    LOAD_COGS = get_settings('LOAD_COGS')

    models = []
    for cog in LOAD_COGS:
        module_name = f'cogs.{cog.lower()}.models'
        try:
            importlib.import_module(module_name)
            models.append(f'cogs.{cog.lower()}.models')
        
        except ModuleNotFoundError:
            pass

    await Tortoise.init(
        db_url=f'sqlite://{DATABASE_PATH}',
        modules={'models': models}
    )
    await Tortoise.generate_schemas()

run_async(init())