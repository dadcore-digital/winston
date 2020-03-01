def get_secret(secret_name, secrets_file):
    """
    Get secret variable or return explicit exception.

    Always return as string, not unicode.

    Must store this in base settings file due to structure of multiple
    settings files, or risk circular imports.
    """
    try:
        return str(secrets_file[secret_name])

    except KeyError:
        error_msg = "Missing %s setting from secrets file" % secrets_file
        raise Exception(error_msg)
