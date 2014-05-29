# Script creates SNMPv1 item for the host with multiplier = 0.125
# Run as:
# python items_create.py -u http://**/ -H host_name -i item_name -o oid -c your_community
#!/usr/bin/python
import sys, os
from zabbix_api import ZabbixAPI
from argparse import ArgumentParser

# Provide all info
zabbixUser = ''
zabbixPass = ''

parser = ArgumentParser()
parser.add_argument('-u', '--zabbixURL', help = 'zabbixURL')
parser.add_argument('-H', '--zabbixHost', help = 'zabbixHost')
parser.add_argument('-o', '--ZabbixOID', help = 'ZabbixOID')
parser.add_argument('-c', '--zabbixCommunity', help = 'zabbixCommunity')
parser.add_argument('-i', '--itemName', help = 'itemName')
args = parser.parse_args()

# Login to the Zabbix API
zapi = ZabbixAPI(server = args.zabbixURL, path = "", log_level = 2)
zapi.login(zabbixUser, zabbixPass)

# Get id of the host (Item => Host)
host=zapi.host.get({
"output":"extend",
    "filter":{
        "host": args.zabbixHost
        }
})[0]["hostid"]

# more about ITEM object you can find : 
# https://www.zabbix.com/documentation/2.2/manual/api/reference/item/object 
# https://www.zabbix.com/documentation/1.8/api/item/get
zapi.item.create({
"type": 1,   				# SNMPv1 agent
"snmp_community": args.zabbixCommunity,	# SNMP community
"snmp_oid": args.ZabbixOID,		# SNMP oid
"hostid": host, 			# id of the host Item will belong to
"description": args.itemName,		# item description
"key_": args.itemName,			# item key
"value_type": 0,			# Type of information of the item, numeric float in our case
"delta": 1,				# 1 - Delta, speed per second;
"multiplier":1,				# chechbox: use custom multiplier		
"formula": 0.125                        # Custom multiplier
})
        
zapi.logout(zabbixUser, zabbixPass)
