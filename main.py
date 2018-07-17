from admin import *
from postNetwork import *
from getNetwork import *
from deleteNetwork import *
from putNetwork import *
import config

# SETUP
# Get X-Auth-Token
config.auth = getToken("", "")

# '''
# Get public network ID and public-subnet subnet ID
result = getSubnets([["name", "public-subnet"]])
print json.dumps(result, indent=4)

pubsub = result['subnets'][0]['id']
pubnet = result['subnets'][0]['network_id']

routerResults = []
networkResults = []
subnetResults = []
portResults = []

# CREATE NETWORK
# Create Router
routerResults.append(newRouter("USER-A", pubnet, pubsub, "10.80.1.131"))
print json.dumps(routerResults, indent=4)

# Create Network
networkResults.append(newNetwork("USER-A-NET1"))
networkResults.append(newNetwork("USER-A-NET2"))
print json.dumps(networkResults, indent=4)

# Create Subnet
subnetResults.append(newSubnet(networkResults[0]['network']['id'], "192.168.101.0/24"))
subnetResults.append(newSubnet(networkResults[1]['network']['id'], "192.168.102.0/24"))
print json.dumps(routerResults, indent=4)

# Add ports to router on subnet
portResults.append(newRouterPort(routerResults[0]['router']['id'], subnetResults[0]['subnet']['id']))
portResults.append(newRouterPort(routerResults[0]['router']['id'], subnetResults[1]['subnet']['id']))
print json.dumps(portResults, indent=4)
# '''

raw_input("Press Enter to continue...")

# '''
# DESTROY NETWORK (Reverse order of CREATE)
# Get X-Auth-Token
config.auth = getToken("a67f74b73fd8478e8181189c9856446f", "labstack")

# Delete ports on router
portResults[0] = delPort(routerResults[0]['router']['id'], portResults[0]['port_id'])
portResults[1] = delPort(routerResults[0]['router']['id'], portResults[1]['port_id'])
print json.dumps(portResults, indent=4)

# Delete Subnets
if delSubnet(subnetResults[0]['subnet']['id']):
    print "Subnet " + subnetResults[0]['subnet']['id'] + " Deleted"
if delSubnet(subnetResults[1]['subnet']['id']):
    print "Subnet " + subnetResults[1]['subnet']['id'] + " Deleted"

# Delete Networks
if delNetwork(networkResults[0]['network']['id']):
    print "Network " + networkResults[0]['network']['id'] + " Deleted"
if delNetwork(networkResults[1]['network']['id']):
    print "Network " + networkResults[1]['network']['id'] + " Deleted"

# Delete Router
if delRouter(routerResults[0]['router']['id']):
    print "Router " + routerResults[0]['router']['id'] + " Deleted"
# '''
