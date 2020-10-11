import requests
from services.settings import get_settings

class Steam:
    
    def __init__(self):
        settings = get_settings(['COGS', 'PLAYING'])

        self.GAME_ID = settings['STEAM_GAME_ID']
        self.API_BASE = 'http://api.steampowered.com'
    
    def get_player_count(self, simulate=False, timeout=120):
        """Get a count all people playing KQB on Steam currently."""
        
        params = {'appid': self.GAME_ID}
        api_path = f'ISteamUserStats/GetNumberOfCurrentPlayers/v0001/?appid={self.GAME_ID}'
        resp = requests.get(
            f'{self.API_BASE}/{api_path}', params=params, timeout=timeout)
        
        if resp.status_code == 200:
            return resp.json()['response']['player_count']
        
        return None


def get_steam_players(timeout=120):
    """
    Return a message indicating the count of players in Steam for KQB.
    """
    steam = Steam()
    player_count = steam.get_player_count(timeout=timeout)

    if player_count:
        msg = f'There are **{player_count}** peple playing *Killer Queen Black* in **Steam** right now.'
    else:
        msg = 'It pains me to report that the Steam API has absolutely bungled this one. No clue what\'s going on.'

    return {
        'count': player_count,
        'msg': msg
    }

