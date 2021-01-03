from services.settings import get_settings

class API:

    def __init__(self):
        self.API_BASE = get_settings(['BUZZ_API', 'BASE_URL'])
    
    def get_matches(self, params):
        return f'{self.API_BASE}/matches/?{params}&format=json'
