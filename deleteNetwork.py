from request import *
import config


def delRouter(routerID):
    result = delData(config.location + ":9696", "/v2.0/routers/"+routerID, config.auth)
    return result


def delNetwork(networkID):
    result = delData(config.location + ":9696", "/v2.0/networks/"+networkID, config.auth)
    return result


def delSubnet(subnetID):
    result = delData(config.location + ":9696", "/v2.0/subnets/"+subnetID, config.auth)
    return result
