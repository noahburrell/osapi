import urllib2
import json


def postData(ip, postLocation, postdata, authToken):
    try:
        url = "http://"+ip+postLocation
        req = urllib2.Request(url, postdata, headers={'Content-type': 'application/json', 'Accept': 'application/json', 'X-Auth-Token': authToken})
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        error_message = e.read()
        return error_message


def getData(ip, getLocation, parameters, authToken):
    try:
        url = "http://"+ip+getLocation+parameters
        print url
        req = urllib2.Request(url, headers={'Accept': 'application/json', 'X-Auth-Token': authToken})
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    except urllib2.HTTPError as e:
        error_message = e.read()
        return error_message
