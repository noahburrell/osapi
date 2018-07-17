from postNetwork import *
from getNetwork import *
import config

# Get public network ID and public-subnet subnet ID
result = getSubnets([["name", "public-subnet"]], True)
pubsub = result[0]['subnets']['id']
pubnet = result[0]['subnets']['network_id']

routerResults = []
networkResults = []
subnetResults = []
portResults = []

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
portResults.append(newPort(routerResults[0]['router']['id'], networkResults[0]['network']['id']))
portResults.append(newPort(routerResults[0]['router']['id'], networkResults[1]['network']['id']))
print json.dumps(portResults, indent=4)
