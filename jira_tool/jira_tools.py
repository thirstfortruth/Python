from jira import JIRA
import json

jira = JIRA('https://jira.atlassian.com')
#SEARCH_STRING = 'project = JRA AND (status = "Open" OR status = "Resolved" OR key="JRASERVER-9")'
SEARCH_STRING = 'project = JRA and type = Suggestion and status = Closed  and key < "JRASERVER-10" and key > "JRASERVER-8"'
#issue = jira.issue('JRA-9')
#print(issue.fields.project.key)             # 'JRA'
#print(issue.fields.issuetype.name)          # 'New Feature'
#print(issue.fields.reporter.displayName)    # 'Mike Cannon-Brookes [Atlassian]'
#print(jira.comments('JRA-9'))
#comment = jira.comment('JRA-9', 17800)
#print(comment.raw['body'])


def fetch_tickets(jira_object, search_string):
    jira_issues = jira_object.search_issues(search_string, maxResults=10, expand='changelog')
    return jira_issues


def print_comment(jira_issues):
    for inner_issue in jira_issues:
        print(inner_issue)
        for issue_comment in jira.comments(inner_issue):
            print(issue_comment.raw['body'])


#issue = jira.issue('JRA-1330')
#print(issue.raw)
print(json.dumps(jira.createmeta(projectKeys='TST')))
#print(jira.createmeta(projectKeys='JRA').raw)
#print(fetch_tickets(jira, SEARCH_STRING))
# print_comment(fetch_tickets(jira, SEARCH_STRING))

