# Script gets ID of the template with name zabbixTemplate,
# filters items that belongs to host_id and template_id,
# updates all items where  snmp_community = old_snmp_community
#!/usr/bin/python
import sys, os
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = '********'
zabbixUser = '*******'
zabbixPass = '********'
zabbixHost = '******'
zabbixTemplate = '***********'
old_snmp_community = '********'
new_snmp+community = '********'

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 0)
zapi.login(zabbixUser, zabbixPass)

# Get id of the host
host=zapi.host.get({
"output":"extend",
    "filter":{
        "host": zabbixHost
        }
})[0]["hostid"]
print "Host id:", host

# Get id of the template
template_id=zapi.template.get({
"output":"extend",
    "filter":{
        "host": zabbixTemplate
        }
})[0]["templateid"]
print "Template id: ", "Template id", template_id 

# select items from items.db where templateid=* and hostid=*
# and snmp_community like 'old_snmp_community'
# more about ITEM object you can find : 
# https://www.zabbix.com/documentation/2.2/manual/api/reference/item/object 
# https://www.zabbix.com/documentation/1.8/api/item/get
for items in zapi.item.get({
"filter": {"templateids": template_id, "hostid": host},
"search": {"snmp_community": old_snmp_community},
      "output":"extend"
}):
    # update items, set  snmp_community=new_snmp_community
    zapi.item.update({
      "itemid": items["itemid"],
      "snmp_community": new_snmp_community
    })
    print "Item descripion: ", items["description"], "Item key_:", items["key_"], "SnMp com: ", items["snmp_community"], "item id", items["itemid"]
        
