#!/usr/bin/python
# import hosts from nocproject csv-exported file to zabbix via API
# and assign template 'TestTemplate' and group 'TestGroup' to them
import csv
from zabbix_api import ZabbixAPI

server="http://127.0.0.1/zabbix"
username="Admin"
password="XXXXX"

zapi = ZabbixAPI(server=server, path="", log_level=6)
zapi.login(username, password)

# Get hosts in the hostgroup
group_id = zapi.hostgroup.get({"filter" : {"name" : 'TestGroup'}})[0]['groupid']

template_id = zapi.template.get({"filter" : {"name" : 'TestTemplate'}})[0]['templateid']

file = open("mo-list.txt",'rb')
reader = csv.DictReader( file )

for line in reader:
    print line['name'],line['address']
    t = zapi.host.create (
    {
        "host": line['name'],
        "interfaces":[{
            "type":1,
                "dns":"",
                "main":1,
                "ip": line['address'],
                "port": 10050,
                "useip": 1,
        }],
        "groups": [{ "groupid": group_id }],
        "templates": [{ "templateid": template_id }],
    })

file.close()
