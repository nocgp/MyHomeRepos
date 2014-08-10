from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = '*****'
zabbixUser = 'Admin'
zabbixPass = '*****'    
zabbixNewHost = 'Zabbix server'
webChkName = 'site www.example.com is not available'
url = 'www.example.com'
required_str = 'Admin'

zapi = ZabbixAPI(server=zabbixServer, path="", log_level=1)
zapi.login(zabbixUser, zabbixPass)

host_id = zapi.host.get({
"filter": {"name": zabbixNewHost}
})[0]["hostid"]

# Create scenario
zapi.webcheck.create({
        "name": webChkName,                     # Name of the web scenario, htzn.obbtest.com
        "hostid": host_id,                      # ID of the host that the web scenario belongs to
        "agent": "Internet Explorer 6.0",
        #"applicationid": "619",                        # ID of the application that the web scenario belongs to
        "steps": [
            {
                "name": webChkName,             # Name of the scenario step
                "url": url,  		        # URL to be checked, http://
                "required": required_str,       # Text that must be present in the response
                "status_codes": 200,            # Ranges of required HTTP status codes separated by commas
                "timeout": 5,                   # Request timeout in seconds. 
                "no": 1                         # Sequence number of the step in a web scenario
            }
                ]
    })


# Create trigger
zapi.trigger.create({
"description": "Site is down for " + webChkName + " on {HOST.NAME}",
        "expression": "{"+ zabbixNewHost +":web.test.fail["+webChkName+"].min(180)}>0",
        "priority": 3

})
