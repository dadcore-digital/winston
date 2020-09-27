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
    
    def __init__(self):
        settings = get_settings(['COGS', 'STREAMING'])

        # Twitch Settings
        self.CLIENT_ID = settings['CLIENT_ID']
        self.OAUTH_TOKEN = settings['OAUTH_TOKEN']
        self.GAME_ID = settings['GAME_ID']
        self.EXCLUDED_STREAMERS = settings['EXCLUDED_STREAMERS']

        self.API_BASE = 'https://api.twitch.tv/helix'
    
    def get_live_streams(self, simulate=False, timeout=120):
        """Get a list of all live twitch streams for KQB."""
        
        if not simulate:
            params = {'game_id': self.GAME_ID}
            headers = {
                'Authorization': f'Bearer {self.OAUTH_TOKEN}',
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
            
            return None

        else:
            return [
                {
                    'id': '39323116014',
                    'user_id': '475987568',
                    'user_name': 'fonzworth_bentley',
                    'game_id': '506455',
                    'type': 'live',
                    'title': 'testing',
                    'viewer_count': 1,
                    'started_at': '2020-08-18T03:11:34Z',
                    'language': 'en',
                    'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_fonzworth_bentley-{width}x{height}.jpg',
                    'tag_ids': ['6ea6bca4-4712-4ab9-a906-e3336a9d8039']
                },
                {
                    'id': '39323156014',
                    'user_id': '473987568',
                    'user_name': 'another_streamer',
                    'game_id': '506455',
                    'type': 'live',
                    'title': 'testing',
                    'viewer_count': 1,
                    'started_at': '2020-08-18T03:11:34Z',
                    'language': 'en',
                    'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_fonzworth_bentley-{width}x{height}.jpg',
                    'tag_ids': ['6ea6bca4-4712-4ab9-a906-e3336a9d8039']
                },                
                {
                    'id': '32',
                    'user_id': '4722387568',
                    'user_name': 'yetanotherperson',
                    'game_id': '506455',
                    'type': 'live',
                    'title': 'testing',
                    'viewer_count': 1,
                    'started_at': '2020-08-18T18:56:34Z',
                    'language': 'en',
                    'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_fonzworth_bentley-{width}x{height}.jpg',
                    'tag_ids': ['6ea6bca4-4712-4ab9-a906-e3336a9d8039']
                },
            ]
