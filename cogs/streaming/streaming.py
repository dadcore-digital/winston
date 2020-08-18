import asyncio
import io
import sys
from random import randint, choice
import re
from pyquery import PyQuery as pq
import discord
import requests
from discord import Embed
from discord.ext import commands
from services.settings import get_settings
from .services import Twitch

class Streaming(commands.Cog):

    def __init__(self, bot):
        settings = get_settings(['COGS', 'STREAMING'])

        # Twitch Settings
        self.CLIENT_ID = settings['CLIENT_ID']
        self.OAUTH_TOKEN = settings['OAUTH_TOKEN']
        self.GAME_ID = settings['GAME_ID']
        self.EXCLUDED_STREAMERS = settings['EXCLUDED_STREAMERS']

        self.API_BASE = 'https://api.twitch.tv/helix'

    @commands.command()
    async def streams(self, context, *args):
        """
        Show a list of all live Twitch streams for game.
        """
        

        params = {'game_id': self.GAME_ID}
        headers = {
            'Authorization': f'Bearer {self.OAUTH_TOKEN}',
            'Client-ID': self.CLIENT_ID
        }
        resp = requests.get(
            f'{self.API_BASE}/streams', params=params, headers=headers)
        
        twitch = Twitch()
        streams = twitch.get_live_streams()

        if streams:
            for stream in streams:
                link = f'https://twitch.tv/{stream["user_name"]}'
                embed = Embed(
                    title=stream['title'], color=0x009051, url=link)
                embed.add_field(name='Streamer', value=stream['user_name'], inline=True)
                embed.add_field(name='Watching', value=stream['viewer_count'], inline=True)
                embed.add_field(name='Started At', value=stream['started_at'], inline=False)
                
                thumbnail = stream['thumbnail_url'].replace('{width}', '').replace('{height}', '')
                embed.set_thumbnail(url=thumbnail)
                
                await context.send(embed=embed)
        else:
            msg = 'Dreadfully sorry, no streams currenty live.'
            await context.send(msg)

