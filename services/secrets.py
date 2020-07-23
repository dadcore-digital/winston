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
        return str(secrets_file[secret_name])

    except KeyError:
        error_msg = 'Missing secrets file.'
        raise Exception(error_msg)
