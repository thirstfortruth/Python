import time
from urllib.parse import urlencode, urlparse
import requests
import math
import sys
import pandas as pd
import datetime
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
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))
USER_ID = '80491907'
token_url = 'https://oauth.vk.com/blank.html#access_token=4412584fcb24a791dfcaebd80bc4030b22b4b9511bdd17f8f5a3222ec8b8842f428ea80764236f17ee9ce&expires_in=86400&user_id=4931934'

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


def get_followers_subquery(user_id):
    print('\n1/3. Start getting followers at: ', datetime.datetime.now())
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
    # upper_limit=26000
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
        followers = followers + response_followers["response"]
        # time.sleep(0.3)
    progress_bar(upper_limit, upper_limit)
    return followers


def get_users_groups_subquery(users_list):
    print('\n2/3. Start getting groups at: ', datetime.datetime.now())
    exec_limit = 25
    counter = 0
    upper_limit = len(users_list)
    while counter < upper_limit:
        progress_bar(counter, upper_limit)
        temp_list = [list(x.keys())[0] for x in users_list[counter:counter+exec_limit]]
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
        try:
            response_groups = requests.post('https://api.vk.com/method/execute', execute_params).json()["response"]
            for i in range(len(temp_list)):
                list(users_list[counter + i].values())[0]['groups'] = response_groups[i]
            counter += exec_limit
            progress_bar(upper_limit, upper_limit)
        except:
            pass
    return users_list


def save_results(details_to_save, file_to_save):
    print("\n3/3. Start saving to file at: ", datetime.datetime.now())
    with open(file_to_save, 'w') as f:
        f.write("USER_ID;SEX;BIRTH_DATE;GROUP_NO" + "\n")
    with open(file_to_save, 'a') as f:
        for user in details_to_save:
            groups = list(user.values())[0]['groups']
            if groups:
                for group in groups:
                    string_to_write = str(list(user.keys())[0]) + \
                                      ';' + \
                                      str(list(user.values())[0]['sex']) + \
                                      ';' + \
                                      str(list(user.values())[0]['bdate']) + \
                                      ';' + \
                                      str(group)
                    f.write(string_to_write+"\n")
    print("\nDone saving! File \"{}\". Time:".format(file_to_save), datetime.datetime.now())


def sex_translate(num):
    sex_mapper = {1: "F", 2: "M", 0: "N"}
    return sex_mapper.get(num)


def calculate_age(birthday):
    b_date = datetime.datetime.strptime(birthday, '%d.%m.%Y')
    age = math.floor(((datetime.datetime.today() - b_date).days / 365))
    return age


def main_cycle():
    followers = get_followers_subquery(USER_ID)
    friends = get_friends(USER_ID)
    followers = followers + friends
    followers_transformed = [{x['id']:{'sex': sex_translate(x['sex']), 'bdate':calculate_age(x['bdate'])}}
                             if 'bdate' in x and x['bdate'].count('.') > 1
                             else {x['id']:{'sex': sex_translate(x['sex']), 'bdate': 0}}
                             for x in followers]
    details_with_groups = get_users_groups_subquery(followers_transformed[0:500])
    save_results(details_with_groups, GROUPS_FILE)



main_cycle()

#write_results(USERS_FILE, followers)
# console output for full extract
# Start getting followers at:  2017-04-15 03:34:48.880773
# Progress: [------------------------------------------------->] 100%
# Start getting groups at:  2017-04-15 03:36:21.886027
# Progress: [------------------------------------------------->] 100%
# Saving results 2017-04-15 10:01:07.133937
# Saving to file groups_output.dat
#
# Done saving! 2017-04-15 10:03:10.019590
#
# Process finished with exit code 0