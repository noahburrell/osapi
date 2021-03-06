from request import *
import json
import config


def newRouter(name, netID, snetID, ip=None, debugging=False):
    if ip is None:
        data = \
            {
                "router": {
                    "tenant_id": config.tennantID,
                    "name": name,
                    "external_gateway_info": {
                        "network_id": netID,
                        "enable_snat": True,
                        "external_fixed_ips": [
                            {
                                "subnet_id": snetID
                            }
                        ]
                    },
                    "admin_state_up": True
                }
            }
    else:
        data = \
            {
                "router": {
                    "tenant_id": config.tennantID,
                    "name": name,
                    "external_gateway_info": {
                        "network_id": netID,
                        "enable_snat": True,
                        "external_fixed_ips": [
                            {
                                "ip_address": ip,
                                "subnet_id": snetID
                            }
                        ]
                    },
                    "admin_state_up": True
                }
            }

    result = postData(config.location+":9696", "/v2.0/routers", json.dumps(data), config.auth)
    if debugging:
        print "Request: "+json.dumps(data, indent=4)
        print "Response: "+json.dumps(result, indent=4)

    return result


def newNetwork(name, debugging=False):
    data = \
        {
            "network": {
                "tenant_id": config.tennantID,
                "name": name,
                "admin_state_up": True,
            }
        }

    result = postData(config.location+":9696", "/v2.0/networks", json.dumps(data), config.auth)

    if debugging:
        print "Request: "+json.dumps(data, indent=4)
        print "Response: "+json.dumps(result, indent=4)

    return result


def newSubnet(netID, cidr, debugging=False):
    data = \
        {
            "subnet": {
                "tenant_id": config.tennantID,
                "network_id": netID,
                "ip_version": 4,
                "cidr": cidr
            }
        }

    result = postData(config.location+":9696", "/v2.0/subnets", json.dumps(data), config.auth)

    if debugging:
        print "Request: "+json.dumps(data, indent=4)
        print "Response: "+json.dumps(result, indent=4)

    return result
