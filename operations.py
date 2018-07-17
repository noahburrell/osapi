
from admin import *
from postNetwork import *
from getNetwork import *
from deleteNetwork import *
from putNetwork import *
import config
import mysql.connector


def checkRouter(uid):
    # Check if the user has a vRouter
    connection = config.database.cursor(dictionary=True)
    connection.execute("SELECT * FROM loginInfo LEFT OUTER JOIN routerTable ON loginInfo.id = routerTable.uid WHERE loginInfo.id = '" + uid + "';")

    result = connection.fetchone()
    if connection.rowcount is not 1:
        raise ValueError('User ID "'+uid+'" does not exist or the database cannot be accessed.')

    # Return the openstack router ID if it exists. If it does not, handle the error where the function is called
    return result['osrid']


def createRouter(uid, pubnet, pubsub):
    # Create a new router for the user
    result = newRouter(uid, pubnet, pubsub)

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


def createNetwork(uid, osrid, name, network):
    netResult = newNetwork(name)

    subnetResult = newSubnet(netResult['network']['id'], network)

    portResult = newRouterPort(osrid, subnetResult['subnet']['id'])

    return

