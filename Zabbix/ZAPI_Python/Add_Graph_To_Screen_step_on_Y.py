from zabbix_api import ZabbixAPI

# !!!!!!!  Add graphs to the given screen vertically : X(0):Y(y+1)
# Provide all info
zabbixServer = '*************'
zabbixUser = '**********'
zabbixPass = '************'
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
    
# Specify grapths
graphs = []
for host in hosts:
    
    for item in zapi.item.get({"output":"extend", "hostids":a[0]['hostid'], "filter":
                               {"key_":
                                ["mysql.slave.seconds_behind_master[15]","mysql.slave.seconds_behind_master[3]",
                    "mysql.slave.seconds_behind_master[4]","mysql.slave.seconds_behind_master[5]",
                    "mysql.slave.seconds_behind_master[6]","mysql.slave.seconds_behind_master[7]",
                    "mysql.slave.seconds_behind_master[30]","mysql.slave.seconds_behind_master[31]",
                    "mysql.slave.seconds_behind_master[35]","mysql.slave.seconds_behind_master[29]",
                    "mysql.slave.seconds_behind_master[28]","mysql.slave.seconds_behind_master[27]",
                    "mysql.slave.seconds_behind_master[26]","mysql.slave.seconds_behind_master[25]",
                    "mysql.slave.seconds_behind_master[24]","mysql.slave.seconds_behind_master[10]"]}
                               }):
        graphs.append(item["itemid"])
        print item["name"]


# # # Get given screen info : hsize, vsize, screenid
screen = zapi.screen.get({"output": "extend", "selectScreenItems": "extend", "filter":{"name": zabbixScreen}})
screen_x = screen[0]["hsize"]
screen_y = screen[0]["vsize"]
screen_id = screen[0]["screenid"]

y_taken_array = []
next_y = 0
for a in zapi.screenitem.get({ "output": "extend",
         "screenids": screen_id}):
         print "screenitem", a["resourceid"], "x=", a["x"],"y=", a["y"]
         y_taken_array.append(int(a["y"]))

for x in sorted(y_taken_array):
    next_y = x
      
if next_y > 0:
        y = int(next_y) + 1
else:
        y = 0
        print y

x = 0
for value in sorted(graphs):
          print "creating graph for", value
          zapi.screenitem.create({
                              "screenid": screen_id,
                              "resourcetype": 1,
                              "resourceid": value,
                              "width": 500,
                              'height': 100,
                              "x": str(x),
                              "y": str(y)
                               })
          y +=1
   

print "Done"
