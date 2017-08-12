import json
import requests
import sys

# depends on the current state of API
MEDIA_TYPE = "application/vnd.github.inertia-preview+json"

TOKEN = ""  # Github token
ORG_NAME = "githubotik-inc"  # organization name on Github

# SNS integration configuration
AWS_KEY = ""
AWS_SECRET = ""
SNS_TOPIC = ""  # this should be ARN of a topic
SNS_REGION = ""  # region where sns topic was created
# see all possible types of events here (https://api.github.com/hooks),
# look for amazonsns
EVENTS = ["issues", "pull_request"]

headers = {
    'Accept': MEDIA_TYPE,
    'Authorization': 'token {}'.format(TOKEN)
}

data = {
    'name': 'amazonsns',
    'config': {
        'aws_key': AWS_KEY,
        'sns_topic': SNS_TOPIC,
        'sns_region': SNS_REGION,
        'aws_secret': AWS_SECRET
    },
    'events': EVENTS,
    'active': True
}


def create_hook(*args):
    for repo in args:
        url = "https://api.github.com/repos/{0}/{1}/hooks".format(ORG_NAME, repo)
        r = requests.post(url, headers=headers, data=json.dumps(data))
        r.raise_for_status()
        print("Repo name: {0}, Status code: {1}".format(repo, r.status_code))


create_hook(*sys.argv[1:])
