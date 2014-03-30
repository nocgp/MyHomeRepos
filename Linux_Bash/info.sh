#!/bin/bash
OUTPUT=/tmp/result_`hostname`.txt
TODAY=$(date +"%A, %d %B %Y")

########################
## Print System info 
OS=`uname -s`
case $OS in
                'Linux')
                        echo Hostname\: `hostname -f` >$OUTPUT
                        #echo Hostname\: `hostname`.`tail -4 /etc/resolv.conf | awk '/search/{print $2}'` >$OUTPUT
                        echo OS name\: `uname -p -o` >> $OUTPUT 2>&1  
                        echo CPU cores\: `cat /proc/cpuinfo | grep processor | wc -l` >> $OUTPUT 2>&1
                        echo CPU model\: `cat /proc/cpuinfo | grep "model name" | uniq | cut -d: -f2,3,4,5 | xargs` >> $OUTPUT 2>&1
                        echo IP\: `/sbin/ifconfig -a  | awk '/inet addr:/ {gsub (/.*127.0.0.1.*/,"") ;print $2}' | sed 's/[addr:]//g' | xargs` >> $OUTPUT 2>&1                         
                        ;;
                'AIX')
                        echo Hostname\: `hostname`.`tail -4 /etc/resolv.conf | awk '/search/{print $2}'` >$OUTPUT
                        echo OS name\: `uname -s -v` >> $OUTPUT 2>&1  
                        echo CPU cores\: `lsdev -Cc processor |wc -l` >> $OUTPUT 2>&1
                        echo CPU type\: `lsattr -El proc0 | awk '/type /{print $2}'` >> $OUTPUT 2>&1
                        echo IP\: `ifconfig -a  | awk '/inet/ {gsub (/.*127.0.0.1.*/,"") ;print $2}' | sed '$d' | xargs` >> $OUTPUT 2>&1
                        ;;
                'SunOS')
                        echo Hostname\: `hostname`.`tail -4 /etc/resolv.conf | awk '/search/{print $2}'` >$OUTPUT
                        echo OS name\: `uname -r -s` >> $OUTPUT 2>&1
                        echo CPU cores\: `kstat cpu_info | grep core_id | awk '{ print $2}' | uniq | wc -l` >> $OUTPUT 2>&1
                        echo CPU type\: `psrinfo -pv` >> $OUTPUT 2>&1
                        echo IP\: `/sbin/ifconfig -a | awk '/inet/{print $2}' | xargs` >> $OUTPUT 2>&1
                        ;;
        esac

#######################
## Print Candle version and MQ version
cd ~candle/registry/
if [ $? == 1 ]; then
    echo IBM Tivoli ver\: candle is not installed >> $OUTPUT 2>&1
else
   CANDL_VERSION=`cat cienv.ver |  grep "ver =" | sed 's/.=/\:/g'`
   echo IBM Tivoli $CANDL_VERSION >> $OUTPUT 2>&1
fi
DSPMVER=`dspmqver | awk '/Version:/{print $0}'`
if [ -n "$DSPMVER" ]; then 
   echo Websphere MQ $DSPMVER >> $OUTPUT 2>&1
else
   echo Websphere MQ\: MQ is not installed >> $OUTPUT 2>&1
fi

########################
## QMGR list and QMGR info
QMGR_NAME=`dspmq | awk '{print $1}' | sed -e 's/QMNAME//g;s/.//;s/.$//'`
echo QMGRs list\: $QMGR_NAME >> $OUTPUT 2>&1

for QMGR_NAMES in $QMGR_NAME; do
	cd /var/mqm/qmgrs/$QMGR_NAMES/ssl/
         if [ $? == 1 ]; then
            echo QMGR info\: QM $QMGR_NAMES is not running at the moment  >> $OUTPUT 2>&1
            echo CLUSTER\: QM $QMGR_NAMES is not running or is not in the cluster >> $OUTPUT 2>&1
            echo CONNAME\: QM $QMGR_NAMES is not running or CLUSRCVR is not defined >> $OUTPUT 2>&1
        else    
        QM=`pwd | sed 's/.*qmgrs//g;s/.//;s/\/ssl//'`
        echo QMGR info\: $QM >> $OUTPUT 2>&1
        QM_CLUS=`echo 'dis chl(TO.VCCK00*) where(chltype EQ CLUSRCVR) CLUSTER' | runmqsc $QM | awk '/CLUSTER\(/;/CONNAME\(/{print $0}' | sed "s/^[ \t]*//;s/(/\: /g;s/)//g"`
        QM_CONM=`echo 'dis chl(TO.VCCK00*) where(chltype EQ CLUSRCVR) CONNAME' | runmqsc $QM | awk '/CLUSTER\(/;/CONNAME\(/{print $0}' | sed "s/^[ \t]*//;s/(/\: /g;s/)//g"`
               if [ -n "${QM_CLUS}"  ]; then
                  echo $QM_CLUS >> $OUTPUT 2>&1
               else 
                  echo CLUSTER\: QM is not running or is not in the cluster >> $OUTPUT 2>&1
               fi
               if [ -n "${QM_CONM}"  ]; then
                  echo $QM_CONM >> $OUTPUT 2>&1
               else
                  echo CONNAME\: QM is not running or CLUSRCVR is not defined >> $OUTPUT 2>&1
               fi
           fi 
########################
## QMGR SSL check 
PW=`echo 'use strict;open(F,"key.sth") || die "Can t open key.sth: $!";my $stash;read F,$stash,1024;my @unstash=map { $_^0xf5 } unpack("C*",$stash);foreach my $c (@unstash) {    last if $c eq 0;    printf "%c",$c;}printf "\n";' | perl`
QMGRLOW=`echo $QMGR_NAMES | tr "[:upper:]" "[:lower:]"`

which runmqakm > /dev/null 2>&1;
## If runmqakm is installed -> use "runmqakm"
if [ $? == 0 ]; then
        gskcmd="runmqakm"
        gskjava="runmqckm"
QMGR_VALID_TO_DATE=`$gskcmd -cert -details -label ibmwebspheremq$QMGRLOW -db key.kdb -type cms -pw $PW | awk -F\: 'NR==8 {print $0}'| cut -d: -f2,3,4 | awk -F/: '{print $NF}'`
       if [ -n "${QMGR_VALID_TO_DATE}" ]; then
          echo ssl\: $QMGR_VALID_TO_DATE >> $OUTPUT 2>&1
          LABEL_LIST=`$gskcmd -cert -list all -db key.kdb -type cms -pw $PW | cut -d! -f2 | awk -F/: '{print $NF}' | sed 's/Certificates found\://g;s/trusted//g' | cut -f2 | sed '/^[[:space:]]*$/d'`
             for LABEL in $LABEL_LIST; do
             VALID_TO_DATE=`$gskcmd -cert -details -label $LABEL -db key.kdb -type cms -pw $PW | awk -F\: 'NR==8 {print $0}' | cut -d: -f2,3,4 | awk -F/: '{print $NF}'`
             ISSUER_ID=`$gskcmd -cert -details -label $LABEL -db key.kdb -type cms -pw $PW | awk -F\: 'NR==5 {print $2}'`
                                if [[ "$VALID_TO_DATE" == "$TODAY" ]]; then
                                        echo $LABEL will expire $VALID_TO_DATE  >> $OUTPUT 2>&1
                                        if [[ "ISSUER_ID" == "*GlobalSign*" ]] || [[ "ISSUER_ID" == "*VeriSign*" ]]; then
                                        echo $LABEL with $ISSUER_ID might be PREMIUM >> $OUTPUT 2>&1
                                        fi
                                fi
              done
         else
          echo ssl\: "key.kdb" not found >> $OUTPUT 2>&1
         fi

else
## If runmqakm is not installed -> use "gsk7capicmd"
        gskcmd="gsk7capicmd"
        gskjava="gsk7cmd"
        QMGR_VALID_TO_DATE=`$gskcmd -cert -details -label ibmwebspheremq$QMGRLOW -db key.kdb -type cms -pw $PW | awk -F\: 'NR==8 {print $0}' | sed "s/^[To \:]*//;s/(/\:/g;s/)//g"`
         if [ -n "${QMGR_VALID_TO_DATE}" ]; then
            echo ssl\: $QMGR_VALID_TO_DATE >> $OUTPUT </dev/null 2>&1
            LABEL_LIST=`$gskcmd -cert -list all -db key.kdb -type cms -pw $PW | cut -d! -f2 | awk -F/: '{print $NF}' | sed 's/Certificates found\://g;s/trusted//g' | cut -f2 | sed '/^[[:space:]]*$/d'`
	     for LABEL in $LABEL_LIST; do
		 VALID_TO_DATE=`$gskcmd -cert -details -label $LABEL -db key.kdb -type cms -pw $PW | awk -F\: 'NR==8 {print $0}'`</dev/null
		 ISSUER_ID=`$gskcmd -cert -details -label $LABEL -db key.kdb -type cms -pw $PW | awk -F\: 'NR==5 {print $2}'`
				if [[ "$VALID_TO_DATE" == "$TODAY" ]]; then
					echo $LABEL will expire $VALID_TO_DATE  >> $OUTPUT 2>&1
					if [[ "ISSUER_ID" == "*GlobalSign*" ]] || [[ "ISSUER_ID" == "*VeriSign*" ]]; then
					echo $LABEL with $ISSUER_ID might be PREMIUM >> $OUTPUT 2>&1
					fi
				fi
	      done
           else
           echo ssl\: "key.kdb" is not found >> $OUTPUT 2>&1
           fi
fi
done
CURHOST=`hostname`

if [ "$CURHOST" == "***" ] || [ "$CURHOST" == "***" ]; then
chmod 777 $OUTPUT
exit 0
else
scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no $OUTPUT username@host_ftp:/tmp/
rm $OUTPUT
fi
exit 0

