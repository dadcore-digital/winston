from services.settings import get_settings

class Buzz:

    def __init__(self):
        self.API_BASE = get_settings(['BUZZ_API', 'BASE_URL'])
        self.LEAGUE = get_settings(
            ['BUZZ_API', 'DEFAULT_LEAGUE']).replace(' ', '+')
        self.SEASON = get_settings(
            ['BUZZ_API', 'DEFAULT_SEASON']).replace(' ', '+')

    def events(self, params):
        return f'{self.API_BASE}/events/?{params}&format=json'

    def matches(self, params):
        return f'{self.API_BASE}/matches/?{params}&format=json'

    def streams(self, params):
        return f'{self.API_BASE}/streams/?{params}&format=json'

    def players(self, params):
        return f'{self.API_BASE}/players/?{params}&format=json'

    def playing(self):
        return f'{self.API_BASE}/playing/?format=json'
