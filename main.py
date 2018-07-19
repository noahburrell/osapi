import argparse
from admin import *
from getNetwork import getSubnets
import operations
import config

# INGEST PARAMETERS
parser = argparse.ArgumentParser("Perform operations on a user's network/s.")
parser.add_argument('-n', type=str, help='Create a new subnet with the specified name')
parser.add_argument('-N', type=str, help='Optionally used in conjunction with -n to override the network address (use CIDR notation')
parser.add_argument('-d', type=int, help='Destroy a network with the specified subnet ID')
parser.add_argument('-vv', dest='debugging', action='store_true')
parser.add_argument('USER_ID', type=str, help='ID of user the operations will be preformed on')
parser.set_defaults(debugging=False)
args = parser.parse_args()


# QUICK DEBUG - SET PARSER ARG OVERRIDES HERE
# args.USER_ID = "1"  # Debugging
# args.n = "test-network"  # Debugging
# args.N = "192.168.100.0/24"  # Debugging
# args.d = "50"  # Debugging
# args.debugging = False  # Debugging


# SETUP
# Get X-Auth-Token
config.auth = getToken(config.userID, config.userPassword)

# Resolve public network ID and public-subnet subnet ID
result = getSubnets([["name", "public-subnet"]], args.debugging)
pubsub = result['subnets'][0]['id']
pubnet = result['subnets'][0]['network_id']

# Make sure the user has a vRouter, as one will be required to do any further.
# If the user does not have a vRouter, try to create one. If one cannot be created, raise an error
# This function will also raise an error if the uid specified cannot be found (ie, there is no registered user with that id)
print "Check user has a vRouter:",
routerID = operations.checkRouter(args.USER_ID, args.debugging)
if routerID is None:
    print "[FALSE]"
    routerID = operations.createRouter(args.USER_ID, pubnet, pubsub, args.debugging)
    if routerID is None:
        raise ValueError('User does not have a router and one was not able to be created. No further operations can be performed.')
    else:
        print "New vRouter successfully created"
else:
    print "[TRUE]"
print "Router ID is: "+routerID


# PERFORM NETWORK OPERATIONS BASED ON PROVIDED ARGUMENTS
# Attempt to create a network using the specified name and network address if applicable
if args.n is not None:
    operations.createNetwork(args.USER_ID, routerID, args.n, args.N, args.debugging)

# Attempt to destroy a network using the subnet id (as defined in our database, not the openstack id) if applicable
if args.d is not None:
    operations.destroyNetwork(args.USER_ID, args.d, args.debugging)
