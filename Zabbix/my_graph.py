#####
# Script creates and adds graphs for host;
# Script will add graph to Screen;
# @ zabbixServer - zabbix server URL;
# @ zabbixHost - host for which new graph will be created;
# @ zabbixScreen - screen, which will be updated
#!/usr/bin/python
import sys, os
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = ''
zabbixUser = ''
zabbixPass = ''
zabbixHost = ''
zabbixScreen = 'Iana_Test'

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 0)
zapi.login(zabbixUser, zabbixPass)

#  get host
host = zapi.host.get({
"output": {"hosts": "hostid"},
"filter": {"host": zabbixHost}
})

# get screen, validate screen name
screen = zapi.screen.get({
"output": "extend",
"filter": {"name": zabbixScreen} })
if screen:
   print "Screen found:", screen[0]["name"]
else:
   sys.exit("Screen not found. please provide valid name")

# validate host name
if host:
    host_id = host[0]["hostid"]
    print("Found host id %s  with name %s " % (host_id, zabbixHost))
    items = []
    for item in zapi.item.get({
        "output": "extend",
        "hostids": host_id,
        "search": {"key_": "system.cpu"} }):
        item_id = item["itemid"]
        items.append(item_id)
        print "Item: ", item["itemid"], item["key_"]
    
      
else:
    sys.exit("Host not found. please provide new one")

