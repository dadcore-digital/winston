from datetime import datetime
import arrow
import re
import requests
from services.settings import get_settings
from ics import Calendar
from discord import Embed

def get_upcoming_matches(minutes='', hours='', days=''):
    """
    Get a list of matches from now until a certain time duration.

    Keyword arguments:
    minutes -- Number of minutes ahead to look for start time of match. (int)
    hours -- Number of hours ahead to look for start time of match. (int)
    days -- Number of days ahead to look for start time of match. (int)
    """
    API_BASE = get_settings(['BUZZ_API', 'BASE_URL'])
    resp = requests.get(
        f'{API_BASE}/matches/?minutes={minutes}&hours={hours}&days={days}&format=json'
    ).json()
    matches = resp['results']

    # If paginated results presented, loop through and get all matches.    
    if resp['next']:
        while True:
            resp = requests.get(resp['next']).json()
            matches.append(['results'])
    
            if not resp['next']:
                break
    return matches

def get_next_match(upcoming_matches):
    """
    Get the very next scheduled match, given a list of matches.

    If there are multiple "next matches", e.g. two or more scheduled at the
    same time, return them all.

    Keyword arguments:
    upcoming_matches -- A list of match dicts to consider as possible next matches
    """
    next_match = []

    for idx, match in enumerate(upcoming_matches):
        if idx == 0:
            next_match.append(match)
        else:
            if match['start_time'] == next_match[0]['start_time']:
                next_match.append(match)

    return next_match

def get_match_embed(match):
    """
    Return dictionary of match times and discord embeds given timelie entry.

    Keyword arguments:
    match -- A match entry returned from the Buzz API.
    """
    circuit = match['circuit']['tier'] + match['circuit']['region']
    title = f"{circuit} {match['away']['name']} @ {match['home']['name']} "
    
    # Trim just in case of wacky long team names
    title = title.ljust(200 - len(title), ' ')
    title += '\n'

    link = ''
    if match['primary_caster']:
        link = match['primary_caster']['stream_link']


    # Caster Information
    casted_by = 'n/a'

    # Primary Caster Name
    if match['primary_caster']:
        casted_by = f"**{match['primary_caster']['name']}**"

        # Co-casters
        if match['secondary_casters']:
            if len(match['secondary_casters']) == 1:
                co_casters = match['secondary_casters'][0]
            else:
                co_casters = "{} and {}".format(", ".join(
                    match['secondary_casters'][:-1]),
                    match['secondary_casters'][-1])
            casted_by += f' _with {co_casters}_'
        
        # Stream Link
        if match['primary_caster']['stream_link']:
            casted_by += f"\n{match['primary_caster']['stream_link']}"

        
    match_time_arrow = arrow.get(match['start_time'])
    match_time = match_time_arrow.to('US/Eastern').format('ddd MMM Do @ h:mmA')
    embed = Embed(title=title, color=0x874efe, url=link)
    embed.add_field(name='Match Time :alarm_clock:', value=f'{match_time} ET')
    embed.add_field(name='Countdown', value=match["time_until"])
    embed.add_field(name='Casted By', value=casted_by, inline=False)
    
    # Away Team
    away_team_title = f":small_blue_diamond: {match['away']['name']}"
    away_team_summary = f"_{match['away']['wins']} Wins, {match['away']['losses']} Losses_"

    away_team_members = "{} and {}".format(", ".join(
        match['away']['members'][:-1]), match['away']['members'][-1]
    ).replace('_', '').replace('*', '')
    away_team_summary += f'\n{away_team_members}'
    embed.add_field(name=away_team_title, value=away_team_summary, inline=False)

    # Home Team
    home_team_title = f":small_orange_diamond: {match['home']['name']}"
    home_team_summary = f"*{match['home']['wins']} Wins, {match['home']['losses']} Losses*"

    home_team_members = "{} and {}".format(", ".join(
        match['home']['members'][:-1]), match['home']['members'][-1]
    ).replace('_', '').replace('*', '')
    home_team_summary += f'\n{home_team_members}'

    embed.add_field(name=home_team_title, value=home_team_summary, inline=False)


    et_match_time = match_time_arrow.to('US/Eastern').format('h:mmA')
    ct_match_time = match_time_arrow.to('US/Central').format('h:mmA')
    mt_match_time = match_time_arrow.to('US/Mountain').format('h:mmA')
    pt_match_time = match_time_arrow.to('US/Pacific').format('h:mmA')
    ht_match_time = match_time_arrow.to('US/Hawaii').format('h:mmA')
    gmt_match_time = match_time_arrow.to('Europe/London').format('h:mmA')
    cet_match_time = match_time_arrow.to('Europe/Berlin').format('h:mmA')
    nzt_match_time = match_time_arrow.to('Pacific/Auckland').format('h:mmA')

    all_match_times = f'>>> :statue_of_liberty: {et_match_time} ET :black_small_square: '
    all_match_times += f' :corn: {ct_match_time} CT :black_small_square: '
    all_match_times += f' :mountain_snow:  {mt_match_time} MT :black_small_square: '
    all_match_times += f' :ocean::  {pt_match_time} PT :black_small_square: '
    all_match_times += f' :coconut:  {ht_match_time} HT :black_small_square: '
    all_match_times += f' :kiwi: {nzt_match_time} NZT  :black_small_square: '
    all_match_times += f' :chocolate_bar: {cet_match_time} CET'

    embed.add_field(name='In Your Timezone', value=all_match_times, inline=False)
    return embed
    