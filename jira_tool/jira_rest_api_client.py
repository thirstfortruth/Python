import requests
import json
import base64

JIRA_BASE_URL='https://jira.atlassian.com'
# JIRA_BASE_URL=''
# JIRA_BASE_URL=''
AUTH_STRING=b'login:password'
ENC_AUTH_STRING='Basic ' + base64.encodestring(AUTH_STRING).decode().replace('\n', '')
HEADER={"Authorization":ENC_AUTH_STRING,
        "Content-Type": "application/json",}
print(HEADER)
# exit(0)
SEARCH_URL=JIRA_BASE_URL+'/rest/api/latest/search'
ISSUE_URL=JIRA_BASE_URL+'/rest/api/latest/issue/'
#SEARCH_STR='project = JRA and status = Closed  and key < "JRASERVER-15" and key > "JRASERVER-8"'
SEARCH_STR='project = II'
MAX_RESULTS=1000
OUTPUT_FILE='C:/Users/user/Downloads/04022018/json_out.json'
jira_session = requests.session()
jira_session.headers = HEADER
try:
    jira_session.post(JIRA_BASE_URL)
    # print("Success")
except:
    print('Unable to connect or authenticate with JIRA server.')
# exit(0)
# parameters = {'jql': SEARCH_STR,
#               'startAt': 0,
#               'maxResults': MAX_RESULTS,
#               # 'fields': 'key,status,assignee,creator,reporter,issuetype,project'}
#               'fields': 'key',
#               'expand': 'changelog'}
# print(requests.get(SEARCH_URL, parameters, headers=HEADER).json())
# exit(0)
def issues_by_jql(jql_string):
    parameters={'jql':SEARCH_STR,
                'startAt':0,
                'maxResults':MAX_RESULTS,
                # 'fields': 'key,status,assignee,creator,reporter,issuetype,project'}
                'fields': 'key',
                'expand': 'changelog'}
    result = jira_session.get(SEARCH_URL,params=parameters).json()
    # print(result)
    total=result['total']
    if (total > MAX_RESULTS):
        iter=1
        while(MAX_RESULTS*iter < total):
            parameters['startAt'] = MAX_RESULTS*iter
            result['issues'] = result['issues']+jira_session.get(SEARCH_URL, params=parameters).json()['issues']
            iter+=1
    return result


# def get_issue_changelog(issue_id):
#     GET_CHANGELOG_URL=ISSUE_URL+str(issue_id)
#     parameters = {'startAt': 0,
#                   'maxResults': MAX_RESULTS,
#                   'expand':'changelog'}
#     result = jira_session.get(GET_CHANGELOG_URL, params=parameters).json()
#     return result


# def append_changelog(all_issues):
#     for issue in all_issues:
#         issue['changelog'] = get_issue_changelog(issue['key'])
#         print(issue)


def save_json_data(output_file, data):
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile)



issues=issues_by_jql(SEARCH_STR)
#append_changelog(issues['issues'])
save_json_data(OUTPUT_FILE,issues)



#print(issues)
# for issue in issues['issues']:
#     print(issue['key'])


