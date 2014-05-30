# Script works for zabbix v2.2 version. 
# Script creates new host in zabbix.hosts table
# Script does it for hosts in ./exported_hosts.csv file
#!/usr/bin/python
import csv
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = 'http://127.0.0.1/zabbix'
zabbixUser = 'Admin'
zabbixPass = 'zabbix'

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 6)
zapi.login(zabbixUser, zabbixPass)

# Open file for reading
file = open("./exported_hosts.csv",'rb')
reader = csv.DictReader( file )

# Creates new host
# interfaces and groups are required fields, for more info please visit:
# https://www.zabbix.com/documentation/2.2/manual/api/reference/host/create
# host object: https://www.zabbix.com/documentation/2.2/manual/api/reference/host/object#host
# host interfaces: https://www.zabbix.com/documentation/2.2/manual/api/reference/hostinterface/object#host_interface
for line in reader:
    print line['host'], line['name'] 
    host = zapi.host.create ({
	"host": line['host'],  		
        "interfaces": [
            {
                "type": 1,		# agent, 2 - SNMP, 3 - IPMI, 4 - JMX
                "main": 1,		# Whether the interface is used as default on the host
                "useip": 0,		# 0 - connect using host DNS name
                "ip": "0.0.0.0",	# IP address used by the interface
                "dns": line['name'],	# DNS name used by the interface
                "port": "10050"		# Port number used by the interface
            }
        ],
        "groups": [
            {
                "groupid": "2"		# select * from zabbix.groups.
            }]        
})

file.close()

