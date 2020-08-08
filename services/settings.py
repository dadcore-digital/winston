import os
import json
from pathlib import Path

def get_settings(settings_name):
    """
    Get settings variable or return explicit exception.

    Always return as string, not unicode.

    Must store this in base settings file due to structure of multiple
    settings files, or risk circular imports.
    """
    # Settings file location
    cwd = os.path.dirname(os.path.realpath(__file__))
    project_dir = str(Path(cwd).parent)
    settings_file = f'{project_dir}/settings.json'

    with open(settings_file) as f:
        settings_file = json.loads(f.read())
    try:
        # A root level setting was requested, passed as a string
        if isinstance(settings_name, str):
            return settings_file[settings_name]
        
        # A list of keys was passed, traverse through dictionary
        # and return last key in dict structure.
        elif isinstance(settings_name, list):            
            settings_dict = {}
            for idx in range(len(settings_name)):
                if idx == 0:
                    settings_dict[settings_name[idx]] = {}
                else:
                    settings_dict[settings_name[idx - 1]] = settings_file[settings_name[idx-1]]

                    # On last iteration, return final key value, minus key name
                    if idx == len(settings_name) - 1:
                        return settings_file[settings_name[idx-1]][settings_name[idx]]
        else:
            raise KeyError

    except KeyError:
        error_msg = 'Missing settings file.'
        raise Exception(error_msg)
