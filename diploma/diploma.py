import time
from urllib.parse import urlencode, urlparse
import requests
import math
import sys
import collections
import pandas as pd
import numpy as np

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
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
token_url = 'https://oauth.vk.com/blank.html#access_token=c2a61400d4b928bc1ea7f35bc8d62b2d3f786b7168eb111d86cd5c3df6f3aaeb6235bab565819fbfb32d4&expires_in=86400&user_id=4931934'
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
    get_params = {'access_token': access_token, 'user_id': user_id, 'v': VERSION, 'fields': "sex,bdate"}
    response = requests.get('https://api.vk.com/method/friends.get', get_params)
    return response.json()['response']['items']


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


def get_groups_members(group):
    params_group_memebers = {'access_token': access_token,
                         'group_id': group,
                         'extended': 0,
                         'v': VERSION}
    response_group_memebers = requests.get('https://api.vk.com/method/groups.getMembers', params_group_memebers).json()
    return response_group_memebers['response']['items']


def write_results(filename, data_to_write):
    with open(filename, 'a') as f:
         for line in data_to_write:
              f.write(str(line)+"\n")


def read_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def get_top_list(input_list, limit):
    df1 = pd.DataFrame({'Groups': input_list})
    result = df1.groupby(['Groups']).size().reset_index().sort_values(by=0, ascending=False).head(limit)
    return result['Groups'].values.tolist()


def get_followers_subquery(user_id):
    followers = []
    current_count = 0
    count = 1000
    offset_step = 1000
    exec_limit = 25
    params_followers_count = {"access_token": access_token,
                              "user_ids": user_id,
                              "fields": "followers_count",
                              "v": VERSION}
    response_followers_count = requests.get('https://api.vk.com/method/users.get', params_followers_count).json()
    followers_count = response_followers_count["response"][0]["followers_count"]
    upper_limit = (math.ceil(followers_count/(offset_step*exec_limit)))*(offset_step*exec_limit)
    upper_limit=26000
    while current_count < upper_limit:
        progress_bar(current_count, upper_limit)
        code = '''var count = ''' + str(count) + ''';
                var user_id = ''' + user_id + ''';
                var version = ''' + VERSION + ''';
                var token = "''' + access_token + '''";
                var offset_followers = ''' + str(current_count) + ''';
                var offset_step = ''' + str(offset_step) + ''';
                var followers = [];
                var i = 1;
                while ( i <= ''' + str(exec_limit) + ''' )
                    {
                        followers = followers + API.users.getFollowers({"access_token": (token),
                                                                        "user_id": (user_id),
                                                                        "count":(count),
                                                                        "offset":(offset_followers + offset_step*i),
                                                                        "fields": "sex,bdate",
                                                                        "v": (version)}).items;
                        i = i + 1;
                    };
                return followers;'''
        current_count += offset_step*exec_limit
        execute_params = {"access_token": access_token,
                          "code": code,
                          "v": VERSION}
        response_followers = requests.post('https://api.vk.com/method/execute', execute_params).json()
        #print(response_followers["response"])
        followers = followers + response_followers["response"]
        time.sleep(0.3)
    progress_bar(upper_limit, upper_limit)
    return followers


def get_users_groups_subquery(users_list):
    users_groups = {}
    exec_limit = 25
    counter = 0
    upper_limit = len(users_list)
    while counter < upper_limit:
        progress_bar(counter, upper_limit)
        temp_list = [list(x.keys())[0] for x in users_list[counter:counter+exec_limit]]
        #print(temp_list)
        code = '''var user_list = ''' + str(temp_list) + ''';
                var version = ''' + VERSION + ''';
                var token = "''' + access_token + '''";
                var i = 0;
                var users_groups = [];
                while ( i < user_list.length )
                    {
                        var user_id = user_list[i];
                        users_groups.push(API.users.getSubscriptions({"access_token": (token),
                                                                                    "user_id": (user_id),
                                                                                    "v": (version)}).groups.items);
                        i = i + 1;
                    };
                return users_groups;'''

        execute_params = {"access_token": access_token,
                          "code": code,
                          "v": VERSION}
        response_groups = requests.post('https://api.vk.com/method/execute', execute_params).json()["response"]
        #print(response_groups)
        # print(list(range(len(temp_list))))
        for i in range(len(temp_list)):
            list(users_list[counter + i].values())[0]['groups'] = response_groups[i]
        # users_list = users_groups + response_groups
        counter += exec_limit
        #time.sleep(0.3)
        progress_bar(upper_limit, upper_limit)
    return users_groups
# print('\nGetting followers...')
# # followers = get_followers(USER_ID)
# # friends = get_friends(USER_ID)
# # followers = followers + friends
# # write_results(USERS_FILE, followers)
# followers = read_file(USERS_FILE)
#
# print('\nGetting groups...')
# # groups = get_followers_groups(followers,  len(followers))
# # write_results(GROUPS_FILE, groups)
# groups = read_file(GROUPS_FILE)
#
# top_groups = get_top_list(groups, 100)
# print(get_groups_members(top_groups[0]))

print('\nGetting followers...')
followers = get_followers_subquery(USER_ID)
friends = get_friends(USER_ID)
followers = followers + friends
# print(followers[0])
followers_transformed = [{x['id']:{'sex': x['sex'], 'bdate':x['bdate']}}
                         if 'bdate' in x
                         else {x['id']:{'sex': x['sex'], 'bdate': 0}}
                         for x in followers]
# print(followers_transformed[0:25])
# followers_transformed=[{24067740: {'sex': 2, 'bdate': '18.1'}},
#                        {223918359: {'sex': 2, 'bdate': '31.10.2001'}},
#                        {340475094: {'sex': 1, 'bdate': 0}},
#                        {249016476: {'sex': 2, 'bdate': '2.7'}},
#                        {422707533: {'sex': 2, 'bdate': '16.4.1999'}},
#                        {260562673: {'sex': 1, 'bdate': '8.3'}},
#                        {357867508: {'sex': 2, 'bdate': '7.3.2003'}},
#                        {251309909: {'sex': 2, 'bdate': '29.11.1976'}},
#                        {422733096: {'sex': 1, 'bdate': 0}},
#                        {422372294: {'sex': 1, 'bdate': 0}},
#                        {320478535: {'sex': 1, 'bdate': '6.7'}},
#                        {422719692: {'sex': 1, 'bdate': '20.6.1999'}},
#                        {422726235: {'sex': 1, 'bdate': '28.6.1997'}},
#                        {292742343: {'sex': 2, 'bdate': 0}},
#                        {422722981: {'sex': 2, 'bdate': 0}},
#                        {422725520: {'sex': 1, 'bdate': 0}},
#                        {219348214: {'sex': 1, 'bdate': '9.5'}},
#                        {422536678: {'sex': 2, 'bdate': 0}},
#                        {377165906: {'sex': 1, 'bdate': '26.6.2003'}},
#                        {151112749: {'sex': 1, 'bdate': '7.6'}},
#                        {193973650: {'sex': 1, 'bdate': '15.8.1974'}},
#                        {312738186: {'sex': 1, 'bdate': '26.7'}},
#                        {134371027: {'sex': 2, 'bdate': '5.8'}},
#                        {39078592: {'sex': 2, 'bdate': '14.2'}},
#                        {385441315: {'sex': 1, 'bdate': 0}}]
followers_ids = [list(x.keys())[0] for x in followers_transformed]
print(get_users_groups_subquery(followers_transformed))
#write_results(USERS_FILE, followers)

