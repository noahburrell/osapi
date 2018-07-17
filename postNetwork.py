from request import *
import json
import config


def newRouter(name, netID, snetID, ip, debugging=False):
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
        print json.dumps(data, indent=4)
        print json.dumps(result, indent=4)

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
        print json.dumps(data, indent=4)
        print json.dumps(result, indent=4)

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
        print json.dumps(data, indent=4)
        print json.dumps(result, indent=4)

    return result


def newPort(deviceID, netID, debugging=False):
    data = \
        {
            "port": {
                "admin_state_up": True,
                "device_id": deviceID,
                "network_id": netID,
                "port_security_enabled": True
            }
        }

    result = postData(config.location + ":9696", "/v2.0/ports", json.dumps(data), config.auth)

    if debugging:
        print json.dumps(data, indent=4)
        print json.dumps(result, indent=4)

    return result
