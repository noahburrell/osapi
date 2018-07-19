
from admin import *
from postNetwork import *
from getNetwork import *
from deleteNetwork import *
from putNetwork import *
import config
import mysql.connector


def checkRouter(uid, debugging=False):
    # Check if the user has a vRouter
    connection = config.database.cursor(dictionary=True)
    connection.execute("SELECT * FROM loginInfo LEFT OUTER JOIN routerTable ON loginInfo.id = routerTable.uid WHERE loginInfo.id = '" + uid + "';")

    result = connection.fetchone()
    if debugging:
        print "Matched user/vRouter: "+json.dumps(result, indent=4)

    if connection.rowcount is not 1:
        raise ValueError('User ID "'+uid+'" does not exist or the database cannot be accessed.')

    # Return the openstack router ID if it exists. If it does not, handle the error where the function is called
    return result['osrid']


def createRouter(uid, pubnet, pubsub, debugging=False):
    # Create a new router for the user
    result = newRouter(uid, pubnet, pubsub, None, debugging)

    # Insert a new row into the database
    connection = config.database.cursor()
    sql = "INSERT INTO routerTable (uid, ipaddr, osrid) VALUES (%s, %s, %s)"
    val = (int(uid), result['router']['external_gateway_info']['external_fixed_ips'][0]['ip_address'], result['router']['id'])
    connection.execute(sql, val)
    config.database.commit();

    # Return true/false based on if a row was inserted into the database
    if connection.rowcount == 1:
        return result['router']['id']
    else:
        return None


def createNetwork(uid, osrid, name, network, debugging=False):
    # Initiate a new SQL connection
    connection = config.database.cursor(dictionary=True)

    # Look up the ID of the router in our DB
    connection.execute("SELECT id FROM routerTable WHERE osrid = '" + osrid + "'")
    rid = connection.fetchone()
    if debugging:
        print json.dumps(rid, indent=4)
    if connection.rowcount is not 1:
        raise ValueError('vRouter ID "' + osrid + '" does not exist or the database cannot be accessed.')
    rid = rid['id']

    print "Creating a new network..."

    # Account for network being none and automatically find valid network
    # Get all networks in use by the specified user, joining the subnet table on the router table and looking up the uid specified in the router table
    connection.execute("SELECT cidr FROM subnetTable INNER JOIN routerTable ON subnetTable.rid = routerTable.id WHERE routerTable.uid = '" + uid + "'")
    addressesInUse = connection.fetchall()
    if debugging:
        print "Found existing networks for this user: "+json.dumps(addressesInUse, indent=4)
    if network is None:
        # Iterate through 192.168.2.0/24 to 192.168.254.0/24 (Private class A range minus commonly used 192.168.0.0/24 and 192.168.1.0/24)
        for i in range(2, 254):
            # Assume the network being tried is not in use
            inUse = False
            if debugging:
                print "Trying: 192.168."+str(i)+".0/24"
            # Try to find the network in the list of used networks (for the specified UID) in the DB
            for address in addressesInUse:
                # Set inUse to true if the network exists in the DB
                if address['cidr'] == "192.168."+str(i)+".0/24":
                    if debugging:
                        print "Already exists!"
                    inUse = True
                    break
            # If the tried network is still not seen as inUse after iterating through DB results, set network to the tried network for use later
            if inUse is False:
                if debugging:
                    print "HIT!"
                network = "192.168."+str(i)+".0/24"
                break
        print "Automatically selecting network: " + network
    else:
        # Verify the manually specified network is not in use
        for address in addressesInUse:
            # Set inUse to true if the network exists in the DB
            if address['cidr'] == network:
                raise ValueError("The specified network is already in use on this router!")
        print "Using manually selected network: " + network

    # If the attempt to generate a network address failed (network is still none), raise an error
    if network is None:
        raise ValueError("No networks available!")

    # Create a new network
    netResult = newNetwork(name, debugging)
    if netResult['network']['id'] is None:
        raise ValueError("Failed to create network")
    print "New network ID is: '"+netResult['network']['id']

    # Create a subnet and associate it to the created network
    subnetResult = newSubnet(netResult['network']['id'], network, debugging)
    if subnetResult['subnet']['id'] is not None:

        # Insert row into subnet table
        sql = "INSERT INTO subnetTable (rid, subname, osnetid, cidr, ossubid) VALUES (%s, %s, %s, %s, %s)"
        val = (rid, name, netResult['network']['id'], network, subnetResult['subnet']['id'])
        connection.execute(sql, val)
        config.database.commit()

        if connection.rowcount is not 1:
            raise ValueError('Failed to insert row into subnet table.')
    else:
        raise ValueError("Failed to create subnet and associate with network")
    print "New subnet ID is: '" + subnetResult['subnet']['id']

    # Lookup the ID of the subnet previously created
    connection.execute("SELECT id FROM subnetTable WHERE ossubid = '" + subnetResult['subnet']['id'] + "'")
    subid = connection.fetchone()
    if connection.rowcount is not 1:
        raise ValueError('Subnet ID "' + subnetResult['subnet']['id'] + '" does not exist or the database cannot be accessed.')
    subid = subid['id']
    if debugging:
        print "Matched to subnet: "+str(subid)

    # Create a port and associate it with a router and subnet
    portResult = newRouterPort(osrid, subnetResult['subnet']['id'], debugging)
    if portResult['port_id'] is not None:
        sql = "INSERT INTO portTable (rid, sid, secid, ipaddr, ospid, osdid) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (int(rid), int(subid), "0", getPorts([["id", str(portResult['port_id'])]])['ports'][0]['fixed_ips'][0]['ip_address'], portResult['port_id'], portResult['id'])  # SecID = 0 is temporary until we evaluate the security implementation
        connection.execute(sql, val)
        config.database.commit()

        if connection.rowcount is not 1:
            raise ValueError('Failed to insert row into port table.')
    else:
        raise ValueError("Failed to create port and associate with router and subnet")
    print "New port ID is: '" + portResult['port_id']

    return


def destroyNetwork(uid, subnetid, debugging=False):
    # Initiate a new SQL connection
    connection = config.database.cursor(dictionary=True)

    # Look up the subnet ID in subnet table and join on the ports table since the port needs to be deleted first (if one exists)
    # Also inner join the router table to lookup the uid to ensure the subnet being deleted is owned by the specified uid. The uid is just a sanity check
    connection.execute("SELECT * FROM subnetTable INNER JOIN routerTable ON subnetTable.rid = routerTable.id LEFT OUTER JOIN portTable ON subnetTable.id = portTable.sid WHERE subnetTable.id = '" + subnetid + "' AND routerTable.uid = '"+uid+"'")
    results = connection.fetchone()
    if connection.rowcount is 0:
        raise ValueError('Subnet ID "' + subnetid + '" does not exist or the database cannot be accessed.')
    if debugging:
        print "Get result where user ID="+uid+" and subnet ID="+subnetid+": "+json.dumps(results, indent=4)

    # Delete port
    delPort(results['osrid'], results['ospid'], debugging)
    connection.execute("DELETE FROM portTable WHERE sid='"+subnetid+"'")
    if connection.rowcount is 0:
        raise ValueError('Could not delete port with sid="' + subnetid + '". Does not exist or the database cannot be accessed.')
    print "Port deleted: "+results['ospid']
    config.database.commit()

    # Delete subnet and parent network (contained in same DB table)
    delSubnet(results['ossubid'])
    delNetwork(results['osnetid'])
    connection.execute("DELETE FROM subnetTable WHERE id='"+subnetid+"'")
    if connection.rowcount is 0:
        raise ValueError('Could not delete subnet with id="' + subnetid + '". Does not exist or the database cannot be accessed.')
    print "Subnet deleted: "+results['ossubid']
    print "Network deleted: " + results['osnetid']
    config.database.commit()

    return
