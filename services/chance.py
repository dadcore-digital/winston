import re
import sys
from random import choice
from PIL import Image
from services.settings import get_settings

def answer_flip_question(call, result, question):
    """
    Provide an answer to a question asked via coin flip.

    The logic here is absolute spaghetti code and I need to fix it.

    Arguments:
    call -- The 'heads' or 'snails' prediction user made. (str)
    result -- Flipped result of coin, 'heads' or 'snails'. (str)
    question -- Question text to respond to.
    """
    question = ' '.join(question)

    settings = get_settings(['COGS', 'CHANCE'])['FLIP']
    YES_VARIATIONS = settings['YES_VARIATIONS']
    NO_VARIATIONS = settings['NO_VARIATIONS']
    SERVERS = settings['SERVERS']
    COLORS = settings['COLORS']
    SET_PHRASES = settings['SET_PHRASES']
    
    # Did we win or lose the fip?
    yes = call == result

    # If requesting to play on server like !flip heads west, make answer verbose
    if question.startswith(tuple(SERVERS)):
        question = f'play on {question}'

    # If requesting to play as color !flip heads blue, make answer verbose
    if question.startswith(tuple(COLORS)):
        question = f'be {question} team'

    # Replace existing punctuation with period.
    question = question.rstrip('?').rstrip('!').rstrip('.')
    question = f'{question}.'

    # First try set phrases.
    for phrase in SET_PHRASES:
        if question.lower().startswith(phrase['stem']):
            if yes:
                question = question.lower().replace(
                    phrase['stem'], phrase['positive'], 1)
                return f'{choice(YES_VARIATIONS)}, {question}'

            else:
                question = question.lower().replace(
                    phrase['stem'], phrase['negative'], 1)
                return f'{choice(NO_VARIATIONS)}, {question}'                    

    # Cover case of should + other personal pronouns and proper names
    if question.lower().startswith('should'):
        pronoun_or_name = question.split(' ')[1]

        # We will need to flip the pronoun/answer order, so
        # first just strip it out
        question = question.replace(pronoun_or_name, '', 1)

        if yes:
            question = question.lower().replace(
                'should', f'{pronoun_or_name} **should**', 1) 
            return f'{choice(YES_VARIATIONS)}, {question}'

        else:
            question = question.lower().replace(
                'should', f'{pronoun_or_name} **shouldn\'t**', 1) 
            return f'{choice(NO_VARIATIONS)}, {question}'

    # When all else fails, try this:
    if yes:
        return f'{choice(YES_VARIATIONS)}, you **should** {question.lower()}'
    else:
        return f'{choice(NO_VARIATIONS)}, you **shouldn\'t** {question.lower()}'
    

def build_dice_roll_image(
    rolls, total_width=1120, row_height=160, dice_per_row=6):
    """
    Given a list of dice pre-rolled, return an image of these rolls.

    Arguments:
    rolls -- A list of dice rolls, such as: ['d6_1', 'd8_2', 'd8_3, 'd20_20'] or
            just ['d4_1']. (list)
    total_width -- Width of image to generate. Default to six 160px wide dice
                   images, 1220 (includes extra margin). (int)
    row_height -- Height of each row of images in pixels (int)
    dice_per_row -- Number of dice to display on each row. (int)
    """
    images = []
    for roll in rolls:
        images.append(Image.open(f'{sys.path[0]}/services/assets/{roll}.png'))

    image = combine_images(images, total_width, row_height, dice_per_row)
    return image

    
def combine_images(
    images, total_width, row_height, images_per_row, bg_color=(255,255,255, 0)):
    """
    Appends images in a wrapping horziontal fashion.

    Arguments:
    images -- A list of PIL images (list) 
    total_width -- Width of image in pixels to generate (int)
    row_height -- Height of each row of images in pixels (int)
    images_per_row -- Number of images to display on each row. (int)
    """    
    if not total_width:
        total_width = sum(widths)

    rows = [
            images[i:i+images_per_row] for i in range(
                0, len(images), images_per_row)
            ]    
    
    total_height = len(rows) * row_height

    new_im = Image.new('RGBA', (total_width, total_height), color=bg_color)

    y = 0

    for idx, row in enumerate(rows):
        x = 0
        y = idx * row_height
        
        for image in row:
            new_im.paste(image, (x, y))
            x += image.size[0]

    return new_im

def get_coin_flip_image(side):
    """
    Return full path to image of a coin flip given the side it should land on.

    Arguments:
    side -- Side of coin to show. 'heads' or 'snails' (str)
    """
    if side not in ['heads', 'snails']:
        raise ValueError
    return f'{sys.path[0]}/services/assets/{side}.gif'
