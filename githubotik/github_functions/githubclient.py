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

    def get_column_id(self, project_name, column_name):
        url = "{0}/projects/{1}/columns".format(
            self.GITHUB_URL, self.get_project_id(project_name))
        colums = self.get_items(url)
        for c in colums:
            if c['name'] == column_name:
                return c['id']
        raise ValueError("No column with such name")

    def add_label(self, repo, number, labels=[]):
        url = "{0}/repos/{1}/{2}/issues/{3}/labels".format(
            self.GITHUB_URL, self.org, repo, number)
        r = requests.post(url, headers=self.headers, data=json.dumps(labels))
        r.raise_for_status()

    def create_card(self, col_id, issue_id):
        url = "{0}/projects/columns/{1}/cards".format(self.GITHUB_URL, col_id)
        data = {'content_id': issue_id, 'content_type': 'Issue'}
        r = requests.post(url, headers=self.headers, data=json.dumps(data))
        if not "Project already has the associated issue" in r.content:
            r.raise_for_status()

# NOTE this is a hack. We cannot add PR card to the projects board using PR's ID.
    def get_pr_id(self, repo, number):
        url = "{0}/repos/{1}/{2}/issues/{3}".format(
            self.GITHUB_URL, self.org, repo, number)
        r = self.get_items(url)
        return r['id']

    def get_card_id(self, col_id, event_content_url):
        url = "{0}/projects/columns/{1}/cards".format(self.GITHUB_URL, col_id)
        cards = self.get_items(url)
        for c in cards:
            if c['content_url'] == event_content_url:
                return c['id']
        raise ValueError("No such card in the specified column")

    def delete_card(self, project_name, column_name, event_content_url):
        col_id = self.get_column_id(project_name, column_name)
        card_id = self.get_card_id(col_id, event_content_url)
        url = "{0}/projects/columns/cards/{1}".format(self.GITHUB_URL, card_id)
        r = requests.delete(url, headers=self.headers)
        r.raise_for_status()

    def move_to_done(self, project_name, start_columns, end_column, event_content_url):
        """Looks for the card in the specified columns and moves it to DONE"""
        for col in start_columns:
            col_id = self.get_column_id(project_name, col)
            try:
                card_id = self.get_card_id(col_id, event_content_url)
            except ValueError:
                pass

        end_col_id = self.get_column_id(project_name, end_column)

        url = "{0}/projects/columns/cards/{1}/moves".format(self.GITHUB_URL, card_id)
        data = {'position': 'top', 'column_id': end_col_id}

        r = requests.post(url, headers=self.headers, data=json.dumps(data))
        r.raise_for_status()

    def move_card(self, project_name, start_column, end_column, event_content_url):
        """Moves the card form one column to another"""
        start_col_id = self.get_column_id(project_name, start_column)
        end_col_id = self.get_column_id(project_name, end_column)

        url = "{0}/projects/columns/cards/{1}/moves".format(
            self.GITHUB_URL, self.get_card_id(start_col_id, event_content_url))
        data = {'position': 'top', 'column_id': end_col_id}

        r = requests.post(url, headers=self.headers, data=json.dumps(data))
        r.raise_for_status()

    def add_pull_request_card(self, project_name, column_name, repo, pr_number, labels = []):
        col_id = self.get_column_id(project_name, column_name)
        # self.add_label(repo, pr_number, labels)
        pr_id = self.get_pr_id(repo, pr_number)
        self.create_card(col_id, pr_id)

    def add_issue_card(self, project_name, column_name, repo, issue_number, issue_id, labels = []):
        col_id = self.get_column_id(project_name, column_name)
        # self.add_label(repo, issue_number, labels)
        self.create_card(col_id, issue_id)
