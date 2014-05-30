# Script exports dns, host name from database to the ./exported_hosts.csv file
#!/usr/bin/python
import csv
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = 'http://127.0.0.1/'
zabbixUser = 'Admin'
zabbixPass = 'zabbix'

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 0)
zapi.login(zabbixUser, zabbixPass)


# Open file for writing,
# Define header rows
f = open("./exported_hosts.csv","wb+")
csv_file = csv.writer(f)
csv_file.writerow(['host', 'name'])

# Select "host", "dns" from zabbix.hosts table where "host" like '%htz%'
# Prints these lines and writes them  to the file
for host in zapi.host.get({
"search": {"host": "htz"},
"output": ["host", "dns"] }):
    print host["host"], host["dns"]     
    csv_file.writerow([host["host"], host["dns"]])
   
f.close()

