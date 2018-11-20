import base64
import json
import os
import requests
import re


class jira:

    def get_project_prefix_from_issue_id(self, issue_id):
        parsed = issue_id.split('-')
        if len(parsed) > 1:
            return parsed[0].upper()

        return None

    def get_issue_id_from_github_payload(self, payload):
        issue_id = None
        pattern = '[A-Z]{2,}-\d+'
        matches = re.search(pattern, payload['pull_request']['head']['ref'])
        if matches is not None:
            issue_id = matches.group(0)

        matches = re.search(pattern, payload['pull_request']['title'])
        if matches is not None:
            issue_id = matches.group(0)

        return issue_id

    def issue_transition_update(self, issue_id, new_transition_id):

        jira_user = os.getenv('JIRA_USER')
        jira_token = os.getenv('JIRA_TOKEN')

        headers = {
            'Content-Type': 'application/json',
            "Authorization": 'Basic ' + base64.b64encode(jira_user + ':' + jira_token)
        }

        payload = json.dumps({
            'transition': {
                'id': new_transition_id
            }
        })

        api = os.getenv('JIRA_API') + '/issue/' + issue_id + '/transitions'

        response = requests.request('POST', api, data=payload, headers=headers)

        if response.status_code == 204:
            return True
        else:
            return False
