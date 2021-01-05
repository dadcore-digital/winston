from services.settings import get_settings

class Buzz:

    def __init__(self):
        self.API_BASE = get_settings(['BUZZ_API', 'BASE_URL'])
    
    def matches(self, params):
        return f'{self.API_BASE}/matches/?{params}&format=json'

    def streams(self, params):
        return f'{self.API_BASE}/streams/?{params}&format=json'
    
     