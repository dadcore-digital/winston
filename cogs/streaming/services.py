import requests
from services.settings import get_settings

class Twitch:
    
    def __init__(self):
        settings = get_settings(['COGS', 'STREAMING'])

        # Twitch Settings
        self.CLIENT_ID = settings['CLIENT_ID']
        self.OAUTH_TOKEN = settings['OAUTH_TOKEN']
        self.GAME_ID = settings['GAME_ID']
        self.EXCLUDED_STREAMERS = settings['EXCLUDED_STREAMERS']

        self.API_BASE = 'https://api.twitch.tv/helix'
    
    def get_live_streams(self):
        """Get a list of all live twitch streams for KQB."""
        params = {'game_id': self.GAME_ID}
        headers = {
            'Authorization': f'Bearer {self.OAUTH_TOKEN}',
            'Client-ID': self.CLIENT_ID
        }
        resp = requests.get(
            f'{self.API_BASE}/streams', params=params, headers=headers)
        
        if resp.status_code == 200:
            streams = resp.json()['data']
                
            # Filter out banned streams
            blessed_streams = []
            for stream in streams:
                if stream['user_name'] not in self.EXCLUDED_STREAMERS:
                    blessed_streams.append(stream)

            return blessed_streams
        
        return None

