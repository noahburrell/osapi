import argparse
from admin import *
from postNetwork import *
from getNetwork import *
from deleteNetwork import *
from putNetwork import *
import operations
import config

# INGEST PARAMETERS
parser = argparse.ArgumentParser("Perform operations on a user's network/s.")

parser.add_argument('-n', type=str, help='Create a new subnet with the specified name')
parser.add_argument('-N', type=str, help='Optionally used in conjunction with -n to override the network address (use CIDR notation')
parser.add_argument('-d', type=int, help='Destroy a network with the specified subnet ID')

parser.add_argument('USER_ID', type=str, help='ID of user the operations will be preformed on')

args = parser.parse_args()

# uid = "1"  # Debugging
args.n = "test-network"  # Debugging
# args.N = "192.168.100.0/24"  # Debugging

# SETUP
# Get X-Auth-Token
config.auth = getToken("a67f74b73fd8478e8181189c9856446f", "labstack")

# Get public network ID and public-subnet subnet ID
result = getSubnets([["name", "public-subnet"]])
# print json.dumps(result, indent=4)  # Debugging

pubsub = result['subnets'][0]['id']
pubnet = result['subnets'][0]['network_id']

# Make sure the user has a vRouter, as one will be required to do any further.
# If the user does not have a vRouter, try to create one. If one cannot be created, raise an error
# This function will also raise an error if the uid specified cannot be found
print "Check user has a vRouter:",
routerID = operations.checkRouter(args.USER_ID)
if routerID is None:
    print "[FALSE]"
    routerID = operations.createRouter(args.USER_ID, pubnet, pubsub)
    if routerID is None:
        raise ValueError('User does not have a router and one was not able to be created. No further operations can be performed.')
    else:
        print "New vRouter successfully created"
else:
    print "[TRUE]"
print "Router ID is: "+routerID

# Attempt to create a network using the specified name and network address (if applicable)
if args.n is not None:
    operations.createNetwork(args.USER_ID, routerID, args.n, args.N)

# Attempt to destroy a network using the subnet id (as defined in our database, not the openstack id)
if args.d is not None:
    operations.destroyNetwork(args.d)

'''
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

# raw_input("Press Enter to continue...")

'''
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
