from __future__ import print_function

from config.config_loader import ConfigLoader
from github_functions.githubclient import GithubClient
import json


def lambda_handler(event, context):
    config = ConfigLoader().config()
    github = GithubClient(config['org'], config['token'], config['media_type'])

    gitevent = json.loads(event['Records'][0]['Sns']['Message'])

    if gitevent['action'] == "opened":
        if 'pull_request' in gitevent:
            github.add_pull_request_card(
                config['project'], config['column_for_open'],
                gitevent['repository']['name'],
                gitevent['pull_request']['number'], config['labels'])
        else:
            github.add_issue_card(
                config['project'], config['column_for_open'],
                gitevent['repository']['name'], gitevent['issue']['number'],
                gitevent['issue']['id'], config['labels'])

    elif gitevent['action'] == "reopened":
        if 'pull_request' in gitevent:
            github.delete_card(
                config['project'], config['column_for_closed'],
                gitevent['pull_request']['issue_url'])
            github.add_pull_request_card(
                config['project'], config['column_for_open'],
                gitevent['repository']['name'],
                gitevent['pull_request']['number'], config['labels'])
        else:
            github.delete_card(
                config['project'], config['column_for_closed'],
                gitevent['issue']['url'])
            github.add_issue_card(
                config['project'], config['column_for_open'],
                gitevent['repository']['name'], gitevent['issue']['number'],
                gitevent['issue']['id'], config['labels'])

    elif gitevent['action'] == "closed":
        if 'pull_request' in gitevent:
            github.move_to_done(
                config['project'],
                [config['column_for_open'], config['column_in_progress']],
                config['column_for_closed'],
                gitevent['pull_request']['issue_url'])
        else:
            github.move_to_done(
                config['project'],
                [config['column_for_open'], config['column_in_progress']],
                config['column_for_closed'], gitevent['issue']['url'])

    elif gitevent['action'] == "assigned":
        if 'pull_request' in gitevent:
            github.move_card(
                config['project'], config['column_for_open'],
                config['column_in_progress'],
                gitevent['pull_request']['issue_url'])
        else:
            github.move_card(
                config['project'], config['column_for_open'],
                config['column_in_progress'], gitevent['issue']['url'])

    return gitevent
