#!/usr/bin/python

# The research leading to these results has received funding from the
# European Commission's Seventh Framework Programme (FP7/2007-13)
# under grant agreement no 257386.
#	http://www.bonfire-project.eu/
# Copyright 2012 Yahya Al-Hazmi, TU Berlin
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License


# this script fetches resource monitoring information from Zabbix-Server 
# through Zabbix-API
#
# To run this script you need to install python-argparse "apt-get install python-argparse"

from zabbix_api import ZabbixAPI
import sys
import datetime
import time
import argparse

def fetch_to_csv(username,password,server,hostname,key,output,datetime1,datetime2,debuglevel):
        zapi = ZabbixAPI(server=server, log_level=debuglevel)
        zapi.login(username, password)
        hostid = zapi.host.get({"filter":{"host":hostname}, "output":"extend"})[0]["hostid"]
        itemid = zapi.item.get({"filter":{"key_":key, "hostid":hostid} , "output":"extend"})
        itemidNr=itemid[0]["itemid"]
        if (output == ''):
            output=hostname+".csv"
        f = open(output, 'w')
        str1="#key;timestamp;value\n"
        
        if (datetime1=='' and datetime2==''):
            str1=str1+key+";"+itemid[0]["lastclock"]+";"+itemid[0]["lastvalue"]+"\n"
            #f.write(str1)
	    print "Only the last value has been fetched, specify t1 or t1 and t2 to fetch more date"
        elif (datetime1!='' and datetime2==''):
            d1=datetime.datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
            timestamp1=time.mktime(d1.timetuple())
            timestamp2=int(round(time.time()))
	    history = zapi.history.get({"history":itemid[0]["value_type"],"time_from":timestamp1,"time_till":timestamp2, "itemids":[itemidNr,], "output":"extend" })
            inc=0
            for h in history:
                str1 = str1 + key + ";" + h["clock"] +";"+h["value"] + "\n"
                inc=inc+1
            print str(inc) +" records has been fetched and saved into: " + output
        elif (datetime1=='' and datetime2!=''):
	    str1=str1+key+";"+itemid[0]["lastclock"]+";"+itemid[0]["lastvalue"]+"\n"
	    print "Only the last value has been fetched, specify t1 or t1 and t2 to fetch more date"
	else:
            d1=datetime.datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
            d2=datetime.datetime.strptime(datetime2,'%Y-%m-%d %H:%M:%S')
            timestamp1=time.mktime(d1.timetuple())
            timestamp2=time.mktime(d2.timetuple())
            history = zapi.history.get({"history":itemid[0]["value_type"],"time_from":timestamp1,"time_till":timestamp2, "itemids":[itemidNr,], "output":"extend" })
            inc=0
            for h in history:
                str1 = str1 + key + ";" + h["clock"] +";"+h["value"] + "\n"
                inc=inc+1
            print str(inc) +" records has been fetched and saved into: " + output
        f.write(str1)
        
parser = argparse.ArgumentParser(description='Fetch history from aggregator and save it into CSV file')
parser.add_argument('-s', dest='server_IP', required=True,
                   help='aggregator IP address')
parser.add_argument('-n', dest='hostname', required=True,
                   help='hostname of the VM')
parser.add_argument('-k', dest='key', required=True,
                   help='zabbix item key')
parser.add_argument('-u', dest='username', default='Admin',
                   help='zabbix username, default Admin')
parser.add_argument('-p', dest='password', default='zabbix',
                   help='zabbix password, default zabbix')
parser.add_argument('-o', dest='output', default='',
                   help='output file name, default hostname.csv')
parser.add_argument('-t1', dest='datetime1', default='',
                   help='begin datetime, use this pattern \'2011-11-08 14:49:43\' if only t1 specified then time period will be t1-now ')
parser.add_argument('-t2', dest='datetime2', default='',
                   help='end datetime, use this pattern \'2011-11-08 14:49:43\'')
parser.add_argument('-v', dest='debuglevel', default=0, type=int,
                   help='log level, default 0')
args = parser.parse_args()

fetch_to_csv(args.username, args.password, "http://"+args.server_IP+"/zabbix", args.hostname, args.key, args.output, args.datetime1,args.datetime2,args.debuglevel)
