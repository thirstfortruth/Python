import time
from urllib.parse import urlencode, urlparse
import requests
import math
import json
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.61'
APP_ID = 5927510
FILENAME = 'users_output.dat'
auth_data = {'client_id': APP_ID,
             'display': 'mobile',
             'response_type': 'token',
             'scope': 'friends,status',
             'v': VERSION}
print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
USER_ID = '80491907'
#exit(0)
#
token_url = ''
#while True:
#    token_url = input('Please enter token URL')
#    if len(token_url) == 0:
#        print('Please enter URL')
#        continue
#    break

o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']


def get_friends(user_id):
    get_params = {'access_token': access_token, 'user_id': user_id, 'v': VERSION}
    response = requests.get('https://api.vk.com/method/friends.get', get_params)
    return response.json()['response']


def get_groups_for_user(user_id):
    params_groups_get = {'access_token': access_token,
                         'user_id': user_id,
                         'extended': 0,
                         'v': VERSION}
    response_groups_get = requests.get('https://api.vk.com/method/groups.get', params_groups_get)
    return response_groups_get.json()


def get_followers(user_id):
    followers = []
    offset = 0
    count = 1000
    params_followers_get = {'access_token': access_token,
                            'user_id': user_id,
                            'count': count,
                            'offset': offset,
                            'v': VERSION}
    response_followers_get = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
    count_followers = response_followers_get['response']['count']
    if count_followers > count:
        for i in range(math.floor(count_followers/count)+1):
            params_followers_get = {'access_token': access_token,
                                    'user_id': user_id,
                                    'count': count,
                                    'offset': offset + count * i,
                                    'v': VERSION}
            response = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
            time.sleep(0.3)
            followers = followers + response['response']['items']
    return followers


friends_data = get_friends(USER_ID)
friends_count, friends = friends_data['count'], friends_data['items']
print('Count: ', friends_count, 'Friends: ', friends)
groups = get_groups_for_user(USER_ID)
print('Groups: ', groups)
followers = get_followers(USER_ID)
print('Followers: ', len(followers))
with open(FILENAME, 'w') as f:
    json.dump(followers, f)
#get_all_overlap(friends['response']['items'])
