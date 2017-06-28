from __future__ import print_function

from config.config_loader import ConfigLoader
from github_functions.githubclient import GithubClient
import json

def lambda_handler(event, context):
    config = ConfigLoader().config()
    github = GithubClient(config['org'], config['token'], config['media_type'])

    gitevent = json.loads(event['Records'][0]['Sns']['Message'])

    if gitevent['action'] == "opened" or gitevent['action'] == "reopened" :
        if 'pull_request' in gitevent:
            github.add_pull_request_card(
                config['project'], config['column'],
                gitevent['repository']['name'],
                gitevent['pull_request']['number'], config['labels'])
        else:
            github.add_issue_card(
                config['project'], config['column'],
                gitevent['repository']['name'], gitevent['issue']['number'],
                gitevent['issue']['id'], config['labels'])
    return gitevent
