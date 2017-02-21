from flask import request
from app.main import main
import json


@main.route("/api/v1/jira/user", methods=['GET'])
def get_user():
    response = {"userId": 114, "groupName": "Newegg Tech", "domainName": "CD Service Backend",
                "self": "http://jira/rest/api/2/user?username=jj51", "name": "jj51",
                "emailAddress": "Jaydon.T.Jin@newegg.com",
                "avatarUrls": {"16x16": "http://jira/secure/useravatar?size=small&avatarId=10122",
                               "48x48": "http://jira/secure/useravatar?avatarId=10122"},
                "displayName": "Jaydon.T.Jin (g-mis.cncd02.Newegg) 42063", "active": True, "timeZone": "Asia/Shanghai",
                "groups": {"size": 9, "items": []}, "expand": "groups"}
    result = json.dumps(response)
    return result
