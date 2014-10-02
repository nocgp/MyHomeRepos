#!/bin/bash

DIRECTORY='/home/Died'
HOST=$(hostname -f)
CMD=$(find /home -maxdepth 1 -name '*.tar.gz')
EMAIL='some@'

if [ -z "$HOST" ]; then
        mail -s "Warning!!! Hostname is not set during rsync" $EMAIL
        exit
fi

if [[ -z "$CMD" ]]; then

        stderr=$(/usr/bin/rsync -arq --bwlimit=2400 --numeric-ids --acls --exclude='SMTH/*' --exclude='Died/*' --exclude='logs/*' --delete /var/www/home/ REMOTE:/mnt/$HOST/ 2>&1 1>/dev/null)
        if (( $stderr )); then
            (echo $stderr) | mail -s "Rsync replication problem on $HOST" $EMAIL
        fi
else
        if [ -d "$DIRECTORY" ]; then
                mv $CMD /home/Died
                
        else
                mkdir /home/Died
                mv $CMD /home/Died
        fi

        stderr=$(/usr/bin/rsync -arq --bwlimit=2400 --numeric-ids --acls --exclude='SMTH/*' --exclude='Died/*' --exclude='logs/*' --delete /var/www/home/ REMOTE:/mnt/$HOST/ 2>&1 1>/dev/null)
                if (( $stderr )); then
                        (echo $stderr) | mail -s "Rsync replication problem on $HOST" $EMAIL
                fi
fi
