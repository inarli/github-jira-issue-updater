import requests
from ipaddress import ip_address, ip_network
import datetime
from src.service.database import database


class helper:
    def check_github_ip(self, src_ip):
        src_ip = ip_address(
            u'{}'.format(src_ip)  # Fix stupid ipaddress issue
        )
        whitelist = requests.get('https://api.github.com/meta').json()['hooks']

        for valid_ip in whitelist:
            if src_ip in ip_network(valid_ip):
                return True
        else:
            return False

    def save_pull_request_review(self, issue_id, pr_id, issue_owner_username, reviewer_username, action):
        try:
            db = database()
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO public.pull_request_reviews(issue_id, pr_id, issue_owner_username,reviewer_username,action,created_on) VALUES(%s,%s,%s,%s,%s,%s)',
                (
                    issue_id, pr_id, issue_owner_username, reviewer_username, action, datetime.datetime.now()
                ))
            conn.commit()
            conn.close()
        except Exception, e:
            print str(e)
