from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '' # Your APP_ID here

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
TOKEN = ''


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'sometext'
        }

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def get_visits_count(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits'
        }
        response_visits = requests.get(url, params, headers=headers)
        visits_count = response_visits.json()['data'][0]['metrics'][0]
        return visits_count

    def get_users(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:pv:users'
        }
        response_users = requests.get(url, params, headers=headers)
        users_count = response_users.json()['data'][0]['metrics'][0]
        return users_count

    def get_page_views(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:pv:pageviews'
        }
        response_visits = requests.get(url, params, headers=headers)
        views_count = response_visits.json()['data'][0]['metrics'][0]
        return views_count

metrika = YandexMetrika(TOKEN)

for counter in metrika.counter_list:
    print("Visits:", metrika.get_visits_count(counter))
    print("Users:", metrika.get_users(counter))
    print("Views:", metrika.get_page_views(counter))
