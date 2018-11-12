import base64
import json
import os
import requests


class jira:

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
