import os
from flask import request, jsonify
from flask_api import FlaskAPI
from flask_api.exceptions import NotAcceptable
from dotenv import load_dotenv

load_dotenv(dotenv_path='./.env')
from src.service.jira import jira
from src.service.helper import helper

application = FlaskAPI(__name__)
jiraservice = jira()
helper = helper()


@application.route('/')
def hello_world():
    return jsonify({'Hello': 'World'})


@application.route('/jira-issue-transition', methods=['POST'])
def jira_issue_transition_update():
    if not helper.check_github_ip(src_ip=request.access_route[0]):
        raise NotAcceptable('Github IP whitelist check failed! IP: {}'.format(request.access_route[0]))

    response = None
    if not request.json or not 'review' in request.json or not 'action' in request.json:
        raise NotAcceptable('Invalid JSON')

    if request.json['review']['state'] == 'changes_requested':
        response = jiraservice.issue_transition_update(issue_id=request.json['pull_request']['head']['ref'],
                                                       new_transition_id=os.getenv('JIRA_TRANSITION_REJECT_ID'))
    elif request.json['review']['state'] == 'approved':
        response = jiraservice.issue_transition_update(issue_id=request.json['pull_request']['head']['ref'],
                                                       new_transition_id=os.getenv('JIRA_TRANSITION_APPROVED_ID'))

    if request.json['review']['state'] == 'approved' or request.json['review']['state'] == 'changes_requested':
        helper.save_pull_request_review(issue_id=request.json['pull_request']['head']['ref'],
                                        pr_id=request.json['pull_request']['number'],
                                        issue_owner_username=request.json['pull_request']['user']['login'],
                                        reviewer_username=request.json['review']['user']['login'],
                                        action=request.json['review']['state'])

    if response:
        return jsonify({'ack': 'OK'})
    else:
        return jsonify({'ack': 'NOT OK'})

    if __name__ == '__main__':
        application.run(debug=True)
