import re

def trim_humanize(humanized_time):
    """Given humanized time from arrow, chop off leading 0 hours / 0 minutes."""
    humanized_time = re.sub(r'^0 days and ', '', humanized_time)
    humanized_time = re.sub(r'^0 hours and ', '', humanized_time)
    humanized_time = re.sub(r'^0 days and ', '', humanized_time)
    humanized_time = re.sub(r'^0 days 0 hours and ', '', humanized_time)    
    humanized_time = re.sub(r'^0 days', '', humanized_time)
    humanized_time = humanized_time.lstrip()

    return humanized_time
