# Script was developed for Zabbix in  order to monitore fs errors
# Item in Zabbix : user parameter "cat /tmp/fs_errors", if>0 - trigger alert

#!/usr/bin/env python
import re,os

messages=open('/var/log/messages','r')
regexes='fs error'
result=open('/tmp/fs_errors','w')

def find_fs_errors():
        match_count = 0
        r=re.compile(regexes)
        for line in messages :
                if r.search(line):
                        match_count = 1
        messages.close()
        result.write(str(match_count))
        result.close()

find_fs_errors()
os.chmod('/tmp/fs_errors', 436)
