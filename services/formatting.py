def format_list_as_commas(word_list):
    """
    Given a list like ['one', 'two', 'three'] return 'one, two, and three'
    
    Arguments:
    word_list -- A list of words to join.
    """
    if len(word_list) > 1:
    
        return "{} and {}".format(", ".join(
            word_list[:-1]), word_list[-1]
        ).replace('_', '').replace('*', '')

    else:
        return word_list[0]