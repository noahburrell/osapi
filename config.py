import mysql.connector

# X-Auth-Token.
auth = ''

# ID of Openstack user preforming operations (probably the admin user)
userID = "a67f74b73fd8478e8181189c9856446f"

# The password associated with the user
userPassword = "labstack"

# TennantID can be found in the OpenStack dashboard under Project -> API Access -> View Credentials -> Project ID
tennantID = '9c391e5391684857b4dbd41c93d50b98'

# Location of the API. Localhost when running through an SSH tunnel or on the controller. Access to port 80 and 9696 required.
location = 'localhost'

# Initialize connection to database
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="telus"
)

# Define various database table name
usertable = "loginInfo"
routertable = "routerTable"
subnettable = "subnetTable"
porttable = "portTable"
devicetable = "deviceTable"
