from flask import request, jsonify
from flask_api import FlaskAPI
from flask_api.exceptions import NotAcceptable,NotFound
from dotenv import load_dotenv

# contants
APPROVED = 'approved'
CHANGES_REQUESTED = 'changes_requested'

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

    if not helper.check_github_pull_request_payload(payload=request.json):
        raise NotAcceptable('Json payload is not valid')

    # detect issue_id
    issue_id = jiraservice.get_issue_id_from_github_payload(payload=request.json)

    if not issue_id:
        raise NotAcceptable('Issue could not detect')

    # new pull request state (approve,changes_request,commented)
    pr_state = request.json['review']['state']

    # get new transition id from env with project prefix.
    transition_id = helper.get_transition_id(pr_state)
    if not transition_id:
        raise NotFound('New transition id not found on your env')

    # send update request to jira API
    response = jiraservice.issue_transition_update(issue_id=issue_id, new_transition_id=transition_id)

    if pr_state in [APPROVED, CHANGES_REQUESTED]:
        pr_number = request.json['pull_request']['number']
        issue_owner_username = request.json['pull_request']['user']['login']
        reviewer_username = request.json['review']['user']['login']
        helper.save_pull_request_review(issue_id=issue_id,
                                        pr_id=pr_number,
                                        issue_owner_username=issue_owner_username,
                                        reviewer_username=reviewer_username,
                                        action=pr_state)

    if response:
        return jsonify({'ack': 'OK'})
    else:
        return jsonify({'ack': 'NOT OK'})

    if __name__ == '__main__':
        application.run(debug=True)
