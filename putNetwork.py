from request import *
import json
import config


def newRouterPort(routerID, subnetID, debugging=False):
    data = \
        {
            "subnet_id": subnetID
        }

    result = putData(config.location + ":9696", "/v2.0/routers/"+routerID+"/add_router_interface", json.dumps(data), config.auth)

    if debugging:
        print "Request: "+json.dumps(data, indent=4)
        print "Response: "+json.dumps(result, indent=4)

    return result


def delPort(routerID, portID, debugging=False):
    data = \
        {
            "port_id": portID
        }

    result = putData(config.location + ":9696", "/v2.0/routers/"+routerID+"/remove_router_interface", json.dumps(data), config.auth)

    if debugging:
        print "Request: "+json.dumps(data, indent=4)
        print "Response: "+json.dumps(result, indent=4)

    return result
