import inspect
import re
from tortoise import Tortoise
from .settings import get_settings

def close():
    """
    Gracefully close connection to database.
    
    Should be called as `await close()`
    """
    return Tortoise.close_connections()


def open():
    """
    Open a connection to database.

    Should be called as `await open()`.

    Does some magic nonsense to determine calling module name,
    so it knows path of models file to load.
    """
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    module = re.search(
        r'/cogs/(.*)/', caller_filename).groups()[0]

    DATABASE_PATH = get_settings('DATABASE_PATH')
    return Tortoise.init(
            db_url=f'sqlite://{DATABASE_PATH}',
            modules={'models': [f'cogs.{module}.models']}
        )

