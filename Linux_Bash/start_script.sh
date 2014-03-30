#!/bin/bash -x
# Script for  remote ssh servers and execute commands
# Script will ssh to the remote servers under `whoami` user
TARGET_EMAIL_ALERTS=mail@box.com
HOSTNAME=`hostname -f`
/dev/null > na_list.txt

cat <<EOF |
# Provide server list below:
EOF
while read line
do
if [ "${line:0:1}" != "#"  ]; then
   if [ "${line}" == "$HOSTNAME" ]; then
   cp ./expect.exp ./info.sh /tmp
   chmod 777 /tmp/info.sh /tmp/expect.exp 
   /tmp/expect.exp
   rm /tmp/info.sh /tmp/expect.exp
else
  scp -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no info.sh expect.exp `sewhoami`@${line}:/tmp
    if [ $? -ne 0 ]; then   
       echo COPY to ${line} FAILED with code $? >> na_list.txt
    fi
  ssh -n -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no `sewhoami`@${line}  "chmod 777 /tmp/info.sh /tmp/expect.exp; /tmp/expect.exp; rm /tmp/info.sh /tmp/expect.exp"
    if [ $? -ne 0 ]; then
       echo  EXECUTION FAILED on ${line} with code $? >> na_list.txt
 fi
fi
fi
done
cat /tmp/result_**.txt > /tmp/serverCheck.txt
echo SUCCESSFULLY CHECKED \:  >> na_list.txt
cat /tmp/serverCheck.txt | awk '/Hostname\:/{print $2}' >> na_list.txt
(cat -b na_list.txt) | mailx -a /tmp/serverCheck.txt -s "RESULT" $TARGET_EMAIL_ALERTS 
rm /tmp/result_**.txt /tmp/serverCheck.txt



