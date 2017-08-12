import json
import requests

GITHUB_URL = 'https://api.github.com'
ORG = "githubotik-inc"
PROJECT = "Backlog"
COLUMN = "TODO"
TOKEN = ""

headers = {
    'Accept': 'application/vnd.github.inertia-preview+json',
    'Authorization': 'token {}'.format(TOKEN),
}


def get_items(url):
    r = requests.get(url, headers=headers)
    return json.loads(r.content)


def list_issues():
    url = "{0}/orgs/{1}/repos?per_page=100".format(GITHUB_URL, ORG)
    repos = get_items(url)
    issues = []
    for r in repos:
        url = "{0}/repos/{1}/{2}/issues?per_page=100".format(GITHUB_URL, ORG, r['name'])
        issues = get_items(url)
        for i in issues:
            yield i['id']


def get_project_id(project_name):
    url = "{0}/orgs/{1}/projects".format(GITHUB_URL, ORG)
    projects = get_items(url)
    for p in projects:
        if p['name'] == project_name:
            return p['id']
    raise ValueError("No project with such name")


def get_column_id(project_name, column_name):
    proj_id = get_project_id(project_name)
    url = "{0}/projects/{1}/columns".format(GITHUB_URL, proj_id)
    colums = get_items(url)
    for c in colums:
        if c['name'] == column_name:
            return c['id']
    raise ValueError("No column with such name")


def create_card(project_name, column_name, issue_id):
    col_id = get_column_id(project_name, column_name)
    url = "{0}/projects/columns/{1}/cards".format(GITHUB_URL, col_id)
    data = {'content_id': issue_id, 'content_type': 'Issue'}
    r = requests.post(url, headers=headers, data=json.dumps(data))
    if not "Project already has the associated issue" in r.content:
        r.raise_for_status()


for i in list_issues():
    create_card(PROJECT, COLUMN, i)
