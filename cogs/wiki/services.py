from discord import Embed

def build_result_embed(result_dict):
    """
    Given a result dictionary, return an Embed of the result for Discord.j

    Dict should have following format:

    Arguments:
    result _dict -- A dictionary representing one wiki search result. Each
                    result should be a unique page in the wiki, typically.

    Example:
        result_dict = {
            'title': 'The Helix Tempple',
            'link': 'https://killerqueenblack.wiki/maps/helix/',
            'summary': 'The helix temple is a map in killer queen black, it..,
            'path': '/maps/helix/',
        }    
    """
    embed = Embed(
        title=result_dict['title'], color=0x874efe, url=result_dict['link'])
    
    embed.add_field(
        name='Page', value=f"[{result_dict['path']}]({result_dict['link']})", inline=False)
    embed.add_field(name='Excerpt', value=result_dict['summary'], inline=False)

    return embed