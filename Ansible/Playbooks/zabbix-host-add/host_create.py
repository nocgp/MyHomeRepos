#!/usr/bin/python
import sys
from zabbix_api import ZabbixAPI

# Provide all info
zabbixServer = 'http://ZABBIX/'
zabbixUser = str(sys.argv[4])
zabbixPass = str(sys.argv[3])
zabbixNewHost = str(sys.argv[1])
newHostDns = str(sys.argv[2])

# Login to the Zabbix API
zapi = ZabbixAPI(server = zabbixServer, path = "", log_level = 6)
zapi.login(zabbixUser, zabbixPass)

host = zapi.host.create ({
        "host": zabbixNewHost,           
        "interfaces": [
            {
                "type": 1,              # agent, 2 - SNMP, 3 - IPMI, 4 - JMX
                "main": 1,              # Whether the interface is used as default on the host
                "useip": 0,             # 0 - connect using host DNS name
                "ip": "0.0.0.0",        # IP address used by the interface
                "dns": newHostDns,    # DNS name used by the interface
                "port": "10050"         # Port number used by the interface
            }
        ],
        "groups": [
            {
                "groupid": "2"          # select * from zabbix.groups. 2 - "Linux servers" group id
            }],
	"templates": [
            {
                "templateid": "10300"	# Template_Linux_General
            },
	    {
                "templateid": "10073" 	# Template App MySQL
            },
	{
                "templateid": "10151"	# Template_NFS_mounts 

            },
	{
                "templateid": "10303"   # Template_Linux_Hetzner

            }
        ]        
})

################### Create item for Template_Backups
zapi.item.create({
      "name":"Mysqldump for /mnt/backup/db/" + str(newHostDns) + "/var/backups/mysql/daily.1/ > 1 day",
      "key_": "vfs.file.time[/mnt/backup/db/" + str(newHostDns) + "/var/backups/mysql/daily.1/sqldump,access]",
      "hostid": "10313", 	# select hostid,host from hosts where host like '%Template_Backups%'
      "trends": 365,
      "delay": 30,
      "interfaceid": "1",
      "type": 0,
      "value_type": 3,
      "history": 7
 })          
     
zapi.trigger.create({ 
     "description": "Mysqldump for /mnt/backup/db/" + str(newHostDns) + "/var/backups/mysql/daily.1 > 1 day",
     "expression": "{Template_Backups:vfs.file.time[/mnt/backup/db/" + str(newHostDns) + "/var/backups/mysql/daily.1/sqldump,access].now(0)}-{Template_Backups:vfs.file.time[/mnt/backup/db/" + str(newHostDns) + "/var/backups/mysql/daily.1/sqldump,access].last(0)}>86400",
     "priority": 2		# Warning
      })     

################## Create item for Template_Rsync_healthcheck
zapi.item.create({
      "name":"File /mnt/" + str(newHostDns) + "/.checkrsync",
      "key_": "vfs.file.time[/mnt/" + str(newHostDns) + "/.checkrsync]",
      "hostid": "10157",        # select hostid,host from hosts where host like '%Template_Rsync_healthcheck%'
      "trends": 365,
      "delay": 3600,
      "interfaceid": "1",
      "type": 0,
      "value_type": 0,
      "history": 7
 })           
      
zapi.trigger.create({       
     "description": "Check file /mnt/" + str(newHostDns) +  "/.checkrsync was not updated on {HOSTNAME}",
     "expression": "{Template_Rsync_healthcheck:vfs.file.time[/mnt/" + str(newHostDns) + "/.checkrsync].delta(#25)}=0",
     "priority": 2
 }) 

################## Create items for Template App MySQL slave
zapi.item.create({
      "name":"Seconds behind master slave" + str(sys.argv[5]),
      "key_": "mysql.slave.seconds_behind_master["  + str(sys.argv[5]) + "]",
      "hostid": "10152",        # select hostid,host from hosts where host like '%Template App MySQL slave%'
      "trends": 365,
      "delay": 30,
      "interfaceid": "1",
      "type": 0,
      "value_type": 0,
      "history": 7
 })

zapi.item.create({
      "name":"Slave IO running slave" + str(sys.argv[5]),
      "key_": "mysql.slave.io_running[" + str(sys.argv[5]) + "]",
      "hostid": "10152",        # select hostid,host from hosts where host like '%Template App MySQL slave%'
      "trends": 365,
      "delay": 30,
      "interfaceid": "1",
      "type": 0,
      "value_type": 4,
      "history": 7 })

zapi.item.create({
      "name":"Slave IO state slave" + str(sys.argv[5]),
      "key_": "mysql.slave.slave_io_state[" +  str(sys.argv[5]) + "]",
      "hostid": "10152",        # select hostid,host from hosts where host like '%Template App MySQL slave%'
      "trends": 365,
      "delay": 30,
      "interfaceid": "1",
      "type": 0,
      "value_type": 0,
      "history": 7 })

zapi.item.create({
      "name":"Slave SQL running slave" + str(sys.argv[5]),
      "key_": "mysql.slave.sql_running[" + str(sys.argv[5]) + "]",
      "hostid": "10152",        # select hostid,host from hosts where host like '%Template App MySQL slave%'
      "trends": 365,
      "delay": 30,
      "interfaceid": "1",
      "type": 0,
      "value_type": 4,
      "history": 7 })

zapi.trigger.create({
     "description": "Database replication failed for slave" + str(sys.argv[5]) + " on {HOSTNAME}",
     "expression": "{Template App MySQL slave:mysql.slave.sql_running[" + str(sys.argv[5]) + "].str(No)}>0 | {Template App MySQL slave:mysql.slave.io_running["  + str(sys.argv[5]) + "].str(No)}>0",
     "priority": 2     
 })

zapi.trigger.create({
     "description": "Mysql slave" + str(sys.argv[5]) + " too far behind the master on {HOSTNAME}",
     "expression": "{Template App MySQL slave:mysql.slave.seconds_behind_master[" + str(sys.argv[5]) + "].min(600)}>7200",
     "priority": 2
 })


