import sys
from zabbix_api import ZabbixAPI

# Adds graph to the given screen using coordinates  Y:X = (X+1 : Y+1)
# Provide all info
zabbixServer = '*******'
zabbixUser = '*******'
zabbixPass = '******'  
zabbixHost = '*****'
zabbixScreen = 'Server Perfomance'
# Login to the Zabbix API
zapi = ZabbixAPI(server=zabbixServer, path="", log_level=0)
zapi.login(zabbixUser, zabbixPass)

host_id = zapi.host.get({"output": "extend","filter": {"host": zabbixHost}})[0]["hostid"]

itemidnum = []
itemproc=[]
itemiowait = []

for a in zapi.item.get({
        "output": "extend",
        "hostids": host_id}):
    if a["name"] == "Processor load":		# specific graph that needs to be added to the screen
        itemproc.append(a["itemid"])
        print a["name"],a["itemid"]
    if a["name"] == "CPU iowait time":
        itemiowait.append(a["itemid"])
        print a["name"],a["itemid"]
    if a["name"] == "Number of processes":
        itemidnum.append(a["itemid"])
        print a["name"],a["itemid"]
        
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": zabbixScreen}})
screen_x = screen[0]["hsize"]
screen_id = screen[0]["screenid"]

next_y = 0
# Calculate x, y of the next screen item
for a in zapi.screenitem.get({ "output": "extend",
         "screenids": screen_id}):
     print "screenitem", a["resourceid"], "x=", a["x"],"y=", a["y"]
     next_y = a["y"]
 
y = int(next_y) + 1
x = 0

# Add these graphs in specific order 
for value in (itemproc[0],itemiowait[0],itemidnum[0]):
     zapi.screenitem.create({
                             "screenid": screen_id,
                             "resourcetype": 1,		# Simple graph
                             "resourceid": value,
                             "width": 500,
                             'height': 100,
                             "x": str(x),
                             "y": str(y)
                             })
     
     x += 1
     if x == screen_x :
         x = 0
         y += 1

print "Done"
