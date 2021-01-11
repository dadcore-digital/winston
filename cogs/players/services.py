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
        current_teams = []
        past_teams = []

        
        for team in player['teams']:
            if team['is_active']:
                current_teams.append(team)
            else:
                past_teams.append(team)

        # Current Teams
        if current_teams:
            current_teams_display = ''
            
            for team in current_teams:
                current_teams_display += f"[{team['circuit_abbrev']}] {team['name']}\n"
            
            current_teams_display = current_teams_display.rstrip('\n')
            
            # Change to non-plural if only on one team currently
            teams_embed_title = 'Teams'
            if len(current_teams) == 1:
                teams_embed_title = 'Team'
                
            embed.add_field(
                name=teams_embed_title, value=f'>>> {current_teams_display}',
                inline=False
            )

        # Past Teams
        if past_teams:
            
            past_team_names = []
            for team in past_teams:
                past_team_names.append(team['name'])    
            
            embed.add_field(
                name='Once Upon A Team',
                value=format_list_as_commas(past_team_names),
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

        # Might have weeded out the only alias in this case
        if aliases:
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
            name='Trophy Shelf',
            value=f'>>> {award_summary}',
            inline=False
        )
    
    return embed
    

