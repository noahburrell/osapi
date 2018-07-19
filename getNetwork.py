from request import *
import json
import config


def getSubnets(parameters, debugging=False):
    parametersText = ""

    for parameter in parameters:
        parametersText = parametersText+parameter[0]+"="+parameter[1]+"&"

    result = getData(config.location + ":9696", "/v2.0/subnets?", parametersText, config.auth)
    if debugging:
        print "Response to: /v2.0/subnets?" + parametersText + "\n" + json.dumps(result, indent=4)

    return result


def getPorts(parameters, debugging=False):
    parametersText = ""

    for parameter in parameters:
        parametersText = parametersText+parameter[0]+"="+parameter[1]+"&"

    result = getData(config.location + ":9696", "/v2.0/ports?", parametersText, config.auth)
    if debugging:
        print "Response to: /v2.0/ports?"+parametersText+"\n"+json.dumps(result, indent=4)

    return result
