from datetime import datetime
import arrow
import re
import requests
from services.settings import get_settings
from services.formatting import format_list_as_commas
from ics import Calendar
from discord import Embed

def get_player_summary_embed(player):
    """
    Return a discord embed of player summary information.

    Keyword arguments:
    player -- A player entry returned from the Buzz API.
    """

    embed = Embed(title=player['name'], color=0xffb60a)

    if player['name_phonetic']:
        embed.add_field(
            name='Actually, It\'s Pronounced',
            value=f"🗣️ {player['name_phonetic']}",
        )

    if player['pronouns']:
        embed.add_field(
            name='Pronouns', value=f"✨ {player['pronouns']}",            
        )
                
    if player['teams']:
        team_names = []

        for team in player['teams']:
            team_names.append(team['name'])

        embed.add_field(
            name='Teams', value=format_list_as_commas(team_names),
            inline=False
        )

    # Social Media
    if player['twitch_username'] or player['discord_username']:
        social = ''

        if player['discord_username']:
            social += f"discord: *@{player['discord_username']}*\n"

        if player['twitch_username']:
            social += f"twitch: *{player['twitch_username']}*\n"

        social = social.rstrip('\n')
        
        embed.add_field(
            name='Internet Personality', value=f'>>> {social}', inline=False
        )

    if player['aliases']:
        aliases = []
                
        for alias in player['aliases']:
            if alias['name'] != player['name']:
                if alias['name'] not in aliases:
                    aliases.append(alias['name'])

        embed.add_field(
            name='Also Answers To',
            value=f'🕵️ {format_list_as_commas(aliases)}',
            inline=False
        )
    
    if player['award_summary']:
        award_summary = ''
        
        for award in player['award_summary']:
            award_summary += f"{award['discord_emoji']} {award['name']} x{award['count']} \n"
        award_summary = award_summary.rstrip('\n')

        embed.add_field(
            name='Awards',
            value=f'>>> {award_summary}',
            inline=False
        )
    
    return embed
    

