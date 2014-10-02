#!/usr/bin/python
import sys, os
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = 'http://ZABBIX/zabbix'
zabbixUser = str(sys.argv[3])
zabbixPass = str(sys.argv[2])
zabbixHost = str(sys.argv[1])
slave = str(sys.argv[5])

# Login to the Zabbix API
zapi = ZabbixAPI(server=zabbixServer, path="", log_level=0)
zapi.login(zabbixUser, zabbixPass)

#  get host id
#  check that given host id exists, exit in other case
#  get graphs of the host
host_id = zapi.host.get({"output": "extend","filter": {"host": zabbixHost}})[0]["hostid"]
if host_id:
    graphs = []
    for graph in zapi.graph.get({"output": "extend", "hostids": host_id, "filter":{"name":['CPU utilization', 'CPU iowait time', 'Memory usage','Number of processes']} }):
        graphs.append(graph["graphid"])
        print "graph", graph["graphid"]
else:
    sys.exit("No host found")

# Get given screen info : hsize, vsize, screenid
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": "Hetzner Perfomance"}})
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

for value in sorted(graphs):
    zapi.screenitem.create({
                            "screenid": screen_id,
                            "resourcetype": 0,
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



# Append "MYSQL slaves: seconds behind master" screen
item_id=zapi.item.get({"output": "extend",
                        "hostids": "10152",     # Template App MySQL slave      
                        "filter":{
                                  "name": "Seconds behind master slave35"
                                  }})[0]["itemid"]
zapi.graph.create({ 
         "name": "Seconds behind master slave" + slave,
         "width": 900,
         "height": 200,
         "gitems": [
             {
                 "itemid": item_id,
                 "color": "00AA00"
             }
                    ]
             })
graphs_repl = []
for graph in zapi.graph.get({"output": "extend", "hostids": "10152", "search":{"name":"Seconds behind master slave" + slave}}):
        graphs_repl.append(graph["graphid"])
        print graph["graphid"], graph["name"] 
        
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": "MYSQL slaves: seconds behind master"}})
screen_x = screen[0]["hsize"]
screen_y = screen[0]["vsize"]
screen_id = screen[0]["screenid"]
 
next_y = []
for a in zapi.screenitem.get({ "output": "extend",
        "screenids": screen_id}):
        next_y.append(int(a["y"]))

free_y = 0
for y in sorted(next_y):
     free_y = y
          
next_pos_y = 0
if free_y > 0:
         next_pos_y = int(free_y) + 1
         print next_pos_y
else:
         next_pos_y = 0
x = 0
for value in graphs_repl:
      zapi.screenitem.create({
                              "screenid": screen_id,
                              "resourcetype": 0,
                              "width": 500,
                               'height': 100,
                              "resourceid": value,
                              "width": 500,
                             'height': 100,
                              "x": str(x),
                              "y": str(next_pos_y)
                              })
      next_pos_y += 1


### Add graphs to "MYSQL servers" screen
mysql_graph = []
for a in zapi.graph.get({"output": "extend", "hostids": host_id, "search":{"name": "Mysql"}}):
        mysql_graph.append(a["graphid"])
        print "graph", a["graphid"], a["name"]


# # Get given screen info : hsize, vsize, screenid
screen = zapi.screen.get({"output": "extend", "search":{"name": "MYSQL servers"}})
screen_x = screen[0]["hsize"]
screen_y = screen[0]["vsize"]
screen_id = screen[0]["screenid"]

# # Calculate x, y of the next screen item
y_taken_array = []
next_y = 0
for a in zapi.screenitem.get({ "output": "extend",
         "screenids": screen_id}):
          y_taken_array.append(int(a["y"]))

for y in sorted(y_taken_array):
    next_y = y
    
free_y = 0
if next_y > 0:
        free_y = int(next_y) + 1
else:
        free_y = 0
        print free_y

x = 0
for value in mysql_graph:
           print "creating graph for", value
           zapi.screenitem.create({"screenid": screen_id,
                              "resourcetype": 0,
                              "resourceid": value,
                              "width": 500,
                              'height': 100,
                              "x": str(x),
                              "y": str(free_y)
                               })
           if str(x) == screen_x:
               x = 0
               y += 1
           else:
               x += 1
               y = 0

### Hetzner traffic stat
graphs = []
for graph in zapi.graph.get({"output": "extend", "hostids": host_id, "filter":
                                 {"name":['Traffic on eth1 in \ out','Traffic on interface eth0 in \ out']} 
                                 }):
        graphs.append(graph["graphid"])
        print "graph", graph["graphid"]

# Get given screen info : hsize, vsize, screenid
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": "Hetzner traffic stat"}})
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

for value in sorted(graphs):
    zapi.screenitem.create({
                            "screenid": screen_id,
                            "resourcetype": 0,
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

