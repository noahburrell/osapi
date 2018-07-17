# X-Auth-Token. To get this token run /opt/stack/scripts/getXAuthToken.sh located on the controller.
auth = \
    ''

# TennantID can be found in the OpenStack dashboard under Project -> API Access -> View Credentials -> Project ID
tennantID = \
    '9c391e5391684857b4dbd41c93d50b98'

# Location of the API. Localhost when running through an SSH tunnel or on the controller. Access to port 80 and 9696 required.
location = \
    'localhost'

mysqlInfo = [
    "10.1.3.4", 3306, "root", ""
]

usertable = "loginInfo"

routertable = "routerTable"

subnettable = "subnetTable"

porttable = "portTable"

devicetable = "deviceTable"