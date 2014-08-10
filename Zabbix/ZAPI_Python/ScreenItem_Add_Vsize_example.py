from zabbix_api import ZabbixAPI

# !!!!!!!  Add graphs to the given screen vertically : X(0):Y(y+1)
# Provide all info
zabbixServer = '**********'
zabbixUser = '**********'
zabbixPass = '**********'
zabbixHost = ['********']  # str(sys.argv[1])
zabbixScreen = 'MYSQL slaves: seconds behind master'

# Login to the Zabbix API
zapi = ZabbixAPI(server=zabbixServer, path="", log_level=0)
zapi.login(zabbixUser, zabbixPass)

hosts = []
for i in zabbixHost:
    a = zapi.host.get({"output": ['host', 'hostid'],"filter": {"host": i}}) 
    hosts.append(a[0]['hostid'])
    print a[0]['hostid'], a[0]['host']
    
graphs = []
for host in hosts:
    
    for a in zapi.graph.get({"output": "extend", "hostids": host, 'filter':{'name':['CPU iowait time' ]}
                             }):
        graphs.append(a["graphid"])
        print "graph", a["graphid"], a["name"]

# # Get given screen info : hsize, vsize, screenid
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": zabbixScreen}})
screen_x = screen[0]["hsize"]
screen_y = screen[0]["vsize"]
screen_id = screen[0]["screenid"]
#  
# # # Calculate x, y of the next screen item
next_y = 0
for a in zapi.screenitem.get({ "output": "extend",
           "screenids": screen_id}):
        print "screenitem", a["resourceid"], "x=", a["x"],"y=", a["y"]
        next_y = a["y"]
#  #  
for y in sorted(next_y):
       next_pos_y = y
#         
if next_y > 0:
           next_pos_y = int(next_y) + 1
else:
           next_pos_y = 0

x = 0
for value in graphs:
      zapi.screenitem.create({
                              "screenid": screen_id,
                              "resourcetype": 0,
                              "width": 500,
                               'height': 100,
                              "resourceid": value,
                              "x": str(x),
                              "y": str(next_pos_y)
                              })
      next_pos_y += 1
