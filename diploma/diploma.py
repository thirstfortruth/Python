import time
from urllib.parse import urlencode, urlparse
import requests
import math
import sys
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.61'
APP_ID = 5927510
GROUPS_FILE = 'groups_output.dat'
USERS_FILE = 'users_output.dat'
auth_data = {'client_id': APP_ID,
             'display': 'mobile',
             'response_type': 'token',
             'scope': 'friends,status',
             'v': VERSION}
print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
USER_ID = '80491907'
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


# took from http://stackoverflow.com/questions/6169217/replace-console-output-in-python
def progress_bar(value, endvalue, bar_length=50):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write("\rProgress: [{0}] {1}%".format(arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()


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
    count = 1000
    params_followers_get = {'access_token': access_token,
                            'user_id': user_id,
                            'count': count,
                            'v': VERSION}
    response_followers_get = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
    count_followers = response_followers_get['response']['count']
    #count_followers = 10000
    max_count = math.ceil(count_followers/count)*count
    print('Total followers: ', max_count)
    if count_followers > count:
        for i in range(0, max_count, count):
            progress_bar(i, max_count)
            params_followers_get = {'access_token': access_token,
                                    'user_id': user_id,
                                    'count': count,
                                    'offset': i,
                                    'v': VERSION}
            try:
                response = requests.get('https://api.vk.com/method/users.getFollowers', params_followers_get).json()
                time.sleep(0.35)
                followers = followers + response['response']['items']
            except:
                time.sleep(0.35)
        progress_bar(max_count, max_count)
    return followers


def get_followers_groups(followers, followers_count):
    groups = []
    count = 200
    response_groups_get = None
    progress_bar(0, followers_count)
    if followers_count > count:
        for i in range(count, followers_count, count):
            progress_bar(i, followers_count)
            try:
                params_groups_get = {'access_token': access_token,
                                     'user_id': followers[i-count: i],
                                     'count': 1000,
                                     'v': VERSION}
                response_groups_get = requests.get('https://api.vk.com/method/groups.get', params_groups_get).json()
                #print(response_groups_get.json())
                groups = groups + response_groups_get['response']['items']
                time.sleep(0.3)
            except:
                #print("response_groups_get, response: ", response_groups_get)
                time.sleep(0.3)
    else:
        try:
            params_groups_get = {'access_token': access_token,
                                 'user_id': followers,
                                 'count': 1000,
                                 'v': VERSION}
            response_groups_get = requests.get('https://api.vk.com/method/groups.get', params_groups_get).json()
            print(response_groups_get)
            groups = groups + response_groups_get['response']['items']
        except:
            print("response_groups_get, response: ", response_groups_get)
    progress_bar(followers_count, followers_count)
    print("\n")
    return groups


def write_results(filename, data_to_write):
    with open(filename, 'a') as f:
         for line in data_to_write:
              f.write(str(line)+"\n")


#friends_data = get_friends(USER_ID)
#friends_count, friends = friends_data['count'], friends_data['items']
#groups = get_groups_for_user(USER_ID)
print('\nGetting followers....')
followers = get_followers(USER_ID)
followers_count = len(followers)
write_results(USERS_FILE, followers)
print('\nGetting groups....')
groups = get_followers_groups(followers, followers_count)
#followers = get_followers(4931934)
print('Got followers. Number: {}. Proceeding with file creation.'.format({followers_count}))
write_results(GROUPS_FILE, groups)

#get_followers_groups(USER_ID)
#print(get_followers_groups(4931934))
