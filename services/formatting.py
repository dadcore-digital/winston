def format_list_as_commas(word_list):
    """
    Given a list like ['one', 'two', 'three'] return 'one, two, and three'
    
    Arguments:
    word_list -- A list of words to join.
    """
    if len(word_list) > 1:
        
        # Strip out any commas first
        for idx, word in enumerate(word_list):
            word_list[idx] = word.replace(',', '')

        return "{} and {}".format(", ".join(
            word_list[:-1]), word_list[-1]
        ).replace('_', '').replace('*', '')

    elif len(word_list) == 1:
        return word_list[0]
    
    return None

def strfdelta(tdelta):
    """
    Format a time delta object to be human readable.

    Arguments:
    tdelta -- Time Delta object to format. (obj)
    """
    delta = {'days': tdelta.days}
    delta['hours'], rem = divmod(tdelta.seconds, 3600)
    delta['minutes'], delta['seconds'] = divmod(rem, 60)
    
    result = ''
    if delta['days'] != 0:
        result += f"{delta['days']} days and "
    if delta['hours'] != 0:
        result += f"{delta['hours']} hours and "
    if delta['minutes'] != 0:
        result += f"{delta['minutes']} minutes"

    result = result.rstrip(' and ')
    return result