from request import *
import json
import config


def getToken(user, password):
    data = \
        {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "id": user,
                            "password": password
                        }
                    }
                },
                "scope": {
                    "system": {
                        "all": True
                    }
                }
            }
        }

    try:
        url = "http://" + config.location + "/identity/v3/auth/tokens"
        req = urllib2.Request(url, json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
        response = urllib2.urlopen(req)
        return response.info().getheader('X-Subject-Token')
    except urllib2.HTTPError as e:
        error_message = e.read()
        print error_message
