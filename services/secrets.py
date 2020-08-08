import os
import json
from pathlib import Path

def get_secret(secret_name):
    """
    Get secret variable or return explicit exception.

    Always return as string, not unicode.

    Must store this in base settings file due to structure of multiple
    settings files, or risk circular imports.
    """
    # Secrets file location
    cwd = os.path.dirname(os.path.realpath(__file__))
    project_dir = str(Path(cwd).parent)
    secrets_file = f'{project_dir}/secrets.json'

    with open(secrets_file) as f:
        secrets_file = json.loads(f.read())
    try:
        # A root level setting was requested, passed as a string
        if isinstance(secret_name, str):
            return str(secrets_file[secret_name])
        
        # A list of keys was passed, traverse through dictionary
        # and return last key in dict structure.
        elif isinstance(secret_name, list):            
            secret_dict = {}
            for idx in range(len(secret_name)):
                if idx == 0:
                    secret_dict[secret_name[idx]] = {}
                else:
                    secret_dict[secret_name[idx - 1]] = secrets_file[secret_name[idx-1]]

                    # On last iteration, return final key value, minus key name
                    if idx == len(secret_name) - 1:
                        return secrets_file[secret_name[idx-1]][secret_name[idx]]
        else:
            raise KeyError

    except KeyError:
        error_msg = 'Missing secrets file.'
        raise Exception(error_msg)
