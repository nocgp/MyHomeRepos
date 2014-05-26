# Script creates web scenarion for host
# !!!!! not working copy
# !/usr/sbin/python
import sys, os
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = ''
zabbixUser = ''
zabbixPass = ''
zabbixHost = ''
zabbixApp = 'web checks'

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 0)
zapi.login(zabbixUser, zabbixPass)

#  get host
host = zapi.host.get({
"output": "extend",
"filter": {"host": zabbixHost}
})
host_id = host[0]["hostid"] 

webChk = zapi.webcheck.create({
"name": "nis1-htz15",
        "applicationid": "654",
        "hostid": host_id,
        "steps": [
            {
                "name": "",
                "url": "http://mycompany.com",
                "status_codes": 200,
                "no": 1
            },
            {
                "name": "Homepage / About",
                "url": "http://mycompany.com/about",
                "status_codes": 200,
                "no": 2
            }
        ]})


