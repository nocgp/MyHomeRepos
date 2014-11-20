# run script as: mail_parser email@example.com hh:mm (time is optional)
# Script parses maillog and prints log in a user friendly format
#!/bin/env python
import re
import sys

email_pattern = sys.argv[1]
file = '/var/log/maillog'
#timestamp = sys.argv[2]
if len(sys.argv) == 3:
   timestamp=sys.argv[2]
else:
   timestamp = ''



def client(line):
    client = re.search(r'(client=)([\w\d\.-]+[\w\d\.-]\[[\d]{1,3}\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3}\]))', line)
    if client:
        print re.search('(\w{3}[^a-zA-Z]+)+', line).group(), re.search('([A-F0-9]{10})(:)', line).group(1), '[Client connected from ip]:' , client.group(2)

def message_id(line):
    msg_id=re.search(r'message-id=<([\w\.-]+@[\w\.-]+)>', line)
    if msg_id:
        print re.search('(\w{3}[^a-zA-Z]+)+', line).group(), re.search('([A-F0-9]{10})(:)', line).group(1), "[Header]:", msg_id.group()

def message_from(line):
    sender = re.search('(from=<)([\w\.-]+@[\w\.-]+)(>)', line)
    number_of_recepients = re.search('(nrcpt=)(\d.)',line)
    if sender: print re.search('(\w{3}[^a-zA-Z]+)+', line).group(), re.search('([A-F0-9]{10})(:)', line).group(1), "[Sender]:", sender.group(2)
    if number_of_recepients: print '[Number of recepients]:', number_of_recepients.group(2)

def message_to(line):
    receiver = re.search('(to=<)([\w\.-]+@[\w\.-]+)(>)', line)
    delays = re.search(r'(delays=)([\d+.\d.]+)([\/])([\d+.\d.]+)([\/])([\d+.\d.]+)([\/])([\d+.\d.]+)',line)
    if receiver: 
	print ''
	print re.search('(\w{3}[^a-zA-Z]+)+', line).group(), re.search('([A-F0-9]{10})(:)', line).group(1), "[Receiver]:", receiver.group(2), '\n[Postfix status]:'
    if delays:
        print '\t[Time before queue manager, including message transmission]:', delays.group(2), '\n','\t[Time in queue manager]:', delays.group(4),\
            '\n','\t[Conn setup time including DNS, HELO and TLS]:', delays.group(6), '\n', '\t[Message transmission time]:',delays.group(8),'\n','\t[Status of the message]:', line.split(',')[5:]

def status(line):
    status = re.search('removed', line)
    if status:
        print re.search('(\w{3}[^a-zA-Z]+)+', line).group(), re.search('([A-F0-9]{10})(:)', line).group(1), "[Message status in postfix queue]:", status.group()
	
# Find transaction id
key_ids = []
def find_transaction_id(line):
    if timestamp is not '':
        if re.search(timestamp, line):
            from_ = re.search(r'(postfix/qmgr\[\d*\]: )([A-F0-9]{10})(: from=<)([\w\.-]+@[\w\.-]+)(>)', line)
            to_ = re.search(r'(postfix/lmtp\[\d*\]: )([A-F0-9]{10})(: to=<)([\w\.-]+@[\w\.-]+)(>)', line)
            if (from_) and (from_.group(2) not in key_ids): 
                key_ids.append(from_.group(2))
            elif (to_) and (to_.group(2) not in key_ids): 
                key_ids.append(to_.group(2))
    else:
        from_ = re.search(r'(postfix/qmgr\[\d*\]: )([A-F0-9]{10})(: from=<)([\w\.-]+@[\w\.-]+)(>)', line)
        to_ = re.search(r'(postfix/lmtp\[\d*\]: )([A-F0-9]{10})(: to=<)([\w\.-]+@[\w\.-]+)(>)', line)
        if (from_) and (from_.group(2) not in key_ids): 
           key_ids.append(from_.group(2))
        elif (to_) and (to_.group(2) not in key_ids): 
           key_ids.append(to_.group(2))

# Find transaction ids
fh = open(file, 'r')
for line in fh:
        if re.search(email_pattern, line):
            find_transaction_id(line)
fh.close()

matches = len(key_ids)
if matches > 0:
    print "NOTE: This mailbox was found ", matches, " times as Sender\Receiver\n"
    print '**************************************'
else:
    print sys.exit("Matches not  found")

# Find all events related to that transaction ids elem in line
new_queued = []
for elem in key_ids:
    for line in open(file,'r'):
        current_id = re.search(r'([A-F0-9]{10})(:)', line)
	curr_time = re.search('(\w{3}[^a-zA-Z]+)+', line).group()
        queued_as = re.search(r'(queued as )([A-F0-9]{10})', line)
	if current_id and (elem == current_id.group(1)):
	    client(line)
	    message_id(line)
	    message_from(line)  
	    message_to(line)
            status(line)
            if (queued_as) and (queued_as.group(2) not in key_ids) and (queued_as.group(2) not in new_queued):
		new_queued.append(queued_as.group(2))
            	print 'Mail server received request on email at ', curr_time ,', curr trans id: ', current_id.group(),'; actual email queued as: ', queued_as.group(2)
	    elif (queued_as) and (queued_as.group(2) in key_ids):
                 print '!!!! This is request to the mail server ', ', actual email queued as: ', queued_as.group(2) 
    print '**************************************'

if len(new_queued)>=1:
	for elem in new_queued:
	 	for line in open(file,'r'):
        		current_id = re.search(r'([A-F0-9]{10})(:)', line)
		        if current_id and (elem == current_id.group(1)):
			    client(line)
		            message_id(line)
		            message_from(line)
		            message_to(line)
		            status(line)
                print '**************************************'

print "\nI am done!"

