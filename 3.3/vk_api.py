import time
from urllib.parse import urlencode, urlparse
import requests

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.62'
# APP_ID = 123456789
# auth_data = {'client_id': APP_ID,
#              'display': 'mobile',
#              'response_type': 'token',
#              'scope': 'friends,status',
#              'v': VERSION}
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
token_url = ''
while True:
    token_url = input('Please enter token URL')
    if len(token_url) == 0:
        print('Please enter URL')
        continue
    break

o = urlparse(token_url)
fragments = dict((i.split('=') for i in o.fragment.split('&')))
access_token = fragments['access_token']


def get_online_friends():
    params = {'access_token': access_token, 'v': VERSION}
    friends_online = requests.get('https://api.vk.com/method/friends.getOnline', params)
    print(friends_online.json())


def get_friends_current_user():
    params_friends = {'access_token': access_token, 'v': VERSION}
    friends_all = requests.get('https://api.vk.com/method/friends.get', params_friends)
    return friends_all.json()


def get_friends(friends_list):
    for friend_id in friends_list: # friends_all.json()['response']['items']:
        get_params = {'access_token': access_token, 'user_id': friend_id, 'v': VERSION}
        response = requests.get('https://api.vk.com/method/friends.get', get_params)
        return response.json()


def get_mutual(source_uid, target_uid):
    params_mut_friends = {'access_token': access_token,
                          'source_uid': source_uid,
                          'target_uid': target_uid,
                          'v': VERSION}
    response_mutual = requests.get('https://api.vk.com/method/friends.getMutual', params_mut_friends)
    return response_mutual.json()


def get_all_overlap(friends_list):
    list_enumerate = enumerate(friends_list)
    for pos, item in list_enumerate:
        for i in range(pos+1, len(friends_list)-1):
            mutual_response = get_mutual(friends_list[pos], friends_list[i])
            # delay to avoid "To many requests in seconds" error
            time.sleep(0.3)
            print('Overlap of users: {user1} and {user2}:'.format(user1=friends_list[pos],
                                                                  user2=friends_list[i]),
                  mutual_response)

friends = get_friends_current_user()
print('Friends: ', friends)
get_all_overlap(friends['response']['items'])
