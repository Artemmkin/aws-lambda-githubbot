import requests
import json

class GithubClient():

    GITHUB_URL = 'https://api.github.com'

    def __init__(self, org, token, media_type):
        self.org = org
        self.headers = {
            'Accept': media_type,
            'Authorization': 'token {}'.format(token),
        }

    def get_items(self, url):
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return json.loads(r.content)

    def get_project_id(self, project_name):
        url = "{0}/orgs/{1}/projects".format(self.GITHUB_URL, self.org)
        projects = self.get_items(url)
        for p in projects:
            if p['name'] == project_name:
                return p['id']
        raise ValueError("No project with such name")

    def get_column_id(self, column_name, proj_id):
        url = "{0}/projects/{1}/columns".format(self.GITHUB_URL, proj_id)
        colums = self.get_items(url)
        for c in colums:
            if c['name'] == column_name:
                return c['id']
        raise ValueError("No column with such name")

## Don't think it's needed, but leaving it just in case
    # def get_labels(self, repo, number):
    #     url = "{0}/repos/{1}/{2}/issues/{3}/labels".format(self.GITHUB_URL, self.org, repo, number)
    #     labels = self.get_items(url)
    #     for i in labels:
    #         yield i['name']

    def add_label(self, repo, number, labels = []):
        url = "{0}/repos/{1}/{2}/issues/{3}/labels".format(self.GITHUB_URL, self.org, repo, number)
        # new_labels = set(labels)^set(self.get_labels(repo,number))
        # r = requests.post(url, headers=self.headers, data=json.dumps(list(new_labels)))
        r = requests.post(url, headers=self.headers, data=json.dumps(labels))
        r.raise_for_status()


    def create_card(self, col_id, issue_id):
        url = "{0}/projects/columns/{1}/cards".format(self.GITHUB_URL, col_id)
        data = {'content_id': issue_id, 'content_type': 'Issue'}
        r = requests.post(url, headers=self.headers, data=json.dumps(data))
        if not "Project already has the associated issue" in r.content:
            r.raise_for_status()

## NOTE this is a hack. We cannot add PR card to the projects board using PR's ID
    def get_pr_id(self, repo, number):
        url = "{0}/repos/{1}/{2}/issues/{3}".format(self.GITHUB_URL, self.org, repo, number)
        r = self.get_items(url)
        return r['id']

    def add_pull_request_card(self, project_name, column_name, repo, pr_number, labels = []):
        proj_id = self.get_project_id(project_name)
        col_id = self.get_column_id(column_name, proj_id)
        self.add_label(repo, pr_number, labels)
        pr_id = self.get_pr_id(repo, pr_number)
        self.create_card(col_id, pr_id)

    def add_issue_card(self, project_name, column_name, repo, issue_number, issue_id, labels = []):
        proj_id = self.get_project_id(project_name)
        col_id = self.get_column_id(column_name, proj_id)
        self.add_label(repo, issue_number, labels)
        self.create_card(col_id, issue_id)
