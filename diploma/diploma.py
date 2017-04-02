import time
from urllib.parse import urlencode, urlparse
import requests
import math
import json
import vk
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
token_url = 'https://oauth.vk.com/blank.html#access_token=f94e416a29050eb5428ba8f14e9bbcdbf1d7988a9411af354ca702e9b76d97ae9fcb32a5e66a42ad39b12&expires_in=86400&user_id=4931934'
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
            try:
                response = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
                time.sleep(0.25)
                followers = followers + response['response']['items']
            except:
                print("get_followers, responce: ", response)
    return followers


def get_followers_groups(user_id):
    followers = []
    offset = 0
    count = 10
    params_followers_get = {'access_token': access_token,
                            'user_id': user_id,
                            'count': count,
                            'offset': offset,
                            'v': VERSION}
    response_followers_get = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
    count_followers = response_followers_get['response']['count']
    if count_followers > count:
        for i in range(math.floor(count_followers/count)+1):
            try:
                params_followers_get = {'access_token': access_token,
                                        'user_id': user_id,
                                        'count': count,
                                        'offset': offset + count * i,
                                        'v': VERSION}
                response = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
                time.sleep(0.33)
                followers = followers + response['response']['items']
                params_groups_get = {'access_token': access_token,
                                     'user_id': response['response']['items'],
                                     'count': 1000,
                                     'v': VERSION}
                response_groups_get = requests.get('https://api.vk.com/method/groups.get', params_groups_get)
                print(response_groups_get.json())
                time.sleep(0.33)
            except:
                print("get_followers, responce: ", response)
                print("response_groups_get, responce: ", response_groups_get.json())
    return followers

#friends_data = get_friends(USER_ID)
#friends_count, friends = friends_data['count'], friends_data['items']
#groups = get_groups_for_user(USER_ID)
# print('Getting followers....')
#followers = get_followers(USER_ID)
followers = [4931934]
print('Got followers. Number: {}. Proceeding with file creation.'.format({len(followers)}))
counter = 0

for follower in followers:
    counter = + 1
    with open(FILENAME, 'a') as f:
        if (counter/len(followers))*100 in range(101, 10):
            print('Task is {percent} done. {count_users} users left'.format(percent=(counter/followers)*100),
                  count_users=counter)
        try:
            groups = get_groups_for_user(follower)
            time.sleep(0.3)
            for group in groups['response']['items']:
                 string_to_write = str(follower)+", "+str(group)
                 f.write(string_to_write+"\n")
        except:
            print(groups)

#get_followers_groups(USER_ID)
print(get_followers_groups(4931934))
