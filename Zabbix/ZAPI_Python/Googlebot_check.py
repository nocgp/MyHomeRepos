# Create Googlebot check
webChkName = 'Googlebot is not blocked for '
pattern = 'htz\d*'

matched = re.search(pattern, zabbixHost)
complete = webChkName + matched.group() +".domain.com"

# # Create scenario
zapi.webcheck.create({
        "name": complete,                     # Name of the web scenario, htzn.obbtest.com
        "hostid": host_id,                      # ID of the host that the web scenario belongs to
        "agent": "Googlebot",
        "http_proxy":"/www.google.com/bot.html",
        "steps": [
               {
                    "name": complete ,             # Name of the scenario step
                    "url": matched.group() + ".domain.com",            # URL to be checked, http://
                    "status_codes": 403,            # Ranges of required HTTP status codes separated by commas
                    "timeout": 5,                   # Request timeout in seconds. 
                    "no": 1                         # Sequence number of the step in a web scenario
                }
                   ]
        })
zapi.trigger.create({
    "description": complete + " on {HOSTNAME}",
    "expression": "{"+zabbixHost +":web.test.fail["+ complete +"].min(180)}>0",
    "priority": 3
     })

