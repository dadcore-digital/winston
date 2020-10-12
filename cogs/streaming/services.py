import arrow
import re
import requests
from discord import Embed
from services.settings import get_settings

def get_stream_embed(stream_dict, view_count=True):

    link = f'https://twitch.tv/{stream_dict["user_name"]}'
    embed = Embed(
        title=stream_dict['title'], color=0x009051, url=link)
    embed.add_field(name='Streamer', value=stream_dict['user_name'], inline=True)
    
    if view_count:
        embed.add_field(name='Watching', value=stream_dict['viewer_count'], inline=True)
    
    present = arrow.utcnow()
    start_time = arrow.get(stream_dict['started_at']) 
    went_live =start_time.humanize(present, granularity=["hour", "minute"])
    went_live = re.sub(r'^0 hours and ', '', went_live)

    embed.add_field(name='Went Live', value=went_live, inline=False)
    
    thumbnail = stream_dict['thumbnail_url'].replace('{width}', '').replace('{height}', '')
    embed.set_thumbnail(url=thumbnail)

    return embed

class Twitch:
    
    def __init__(self, bot=None):
        settings = get_settings(['COGS', 'STREAMING'])

        # Twitch Settings
        self.CLIENT_ID = settings['CLIENT_ID']
        self.CLIENT_SECRET = settings['CLIENT_SECRET']
        self.GAME_ID = settings['GAME_ID']
        self.EXCLUDED_STREAMERS = settings['EXCLUDED_STREAMERS']

        self.API_BASE = 'https://api.twitch.tv/helix'
        
        # Use to persist oauth access token as global variable
        self.bot = bot

    def get_access_token(self):
        """
        Use 
        """
        url ='https://id.twitch.tv/oauth2/token'
        data = {
                'client_id': self.CLIENT_ID,
                'client_secret': self.CLIENT_SECRET,
                'grant_type': 'client_credentials',
                'scope': ''
        }
        req = requests.post(url, data)
        access_token = req.json()['access_token']
        
        # Store as global variable for later use. Also allow to use this object
        # bot-less manually for manual hand debugging, so making it optional.
        if self.bot:
            self.bot.twitch_access_token = access_token
        
        return access_token

    def get_live_streams(self, simulate=False, timeout=120):
        """Get a list of all live twitch streams for KQB."""

        params = {'game_id': self.GAME_ID}
        
        try:
            access_token = self.bot.twitch_access_token
        except AttributeError:
            access_token = self.get_access_token()

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Client-ID': self.CLIENT_ID
        }
        resp = requests.get(
            f'{self.API_BASE}/streams', params=params, headers=headers, timeout=timeout)
        
        if resp.status_code == 200:
            streams = resp.json()['data']
                
            # Filter out banned streams
            blessed_streams = []
            for stream in streams:
                if stream['user_name'] not in self.EXCLUDED_STREAMERS:
                    blessed_streams.append(stream)

            return blessed_streams
        
        # Access token has expired, at least set it up for next time to work
        elif resp.status_code == 401:
            self.get_access_token() 
        
        return None

       
