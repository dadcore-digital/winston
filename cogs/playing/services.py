import requests

def get_steam_players(player_count):
    """
    Return a message indicating the count of players in Steam for KQB.
    """
    if player_count:
        msg = f'There are **{player_count}** peple playing *Killer Queen Black* in **Steam** right now.'
    else:
        msg = 'It pains me to report that the Steam API has absolutely bungled this one. No clue what\'s going on.'

    return {
        'count': player_count,
        'msg': msg
    }

