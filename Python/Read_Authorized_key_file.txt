# Script reads /root/.ssh/authorized_keys or /root/.ssh/authorized_keys2
# Logs all it does to /tmp/authorized_keys_log_file on the server from where you started the script
# How to Run
#    copy file to admindesk.gpserver.dk to /tmp
#    define variables below
#    start script as: python script_name
import paramiko, time, os
from paramiko.ssh_exception import SSHException, BadHostKeyException, AuthenticationException
from socket import error as socket_error

#### Please define these variables below.
backup_dir = '/root/.ssh/trash'
authorized_keys = '/root/.ssh/authorized_keys'
authorized_keys2 = '/root/.ssh/authorized_keys2'
log_file = '/tmp/authorized_keys_log_file'

host_list = ['list', 'hosts']
################################################

def remote_file_does_not_exist(sftp, file_to_check):
    try: sftp.stat(file_to_check)
    except (IOError) as e:
        if e[0] == 2: return True
        else: return False

def if_log_does_not_exist(log_file):
    if not os.path.exists(log_file): return True
    else: return False

if if_log_does_not_exist(log_file):
    log = open(log_file,'a').close()
    log = open(log_file,'a')
else:
    log = open(log_file,'w').close()
    log = open(log_file,'a')
print 'ALL steps will be logged to std_out and to the \nfile', log_file,'on the server from where you started the script\n'
for remote_host in host_list:
    try:
        SSH = paramiko.SSHClient()
        SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SSH.connect(remote_host)
        SFTP = SSH.open_sftp()

        print "ssh is OK to", remote_host
        log.write('\nssh is OK to ' + remote_host)

        # Choose and backup authorized_keys/authorized_keys2
        if remote_file_does_not_exist(SFTP, authorized_keys):
            print 'Choosing authorized_keys file: "', authorized_keys, '" does not exist.. Open "',authorized_keys2,'"'
            log.write('\nChoosing authorized_keys file: "' + authorized_keys + '" does not exist.. Open "'
                      + authorized_keys2 + '"')
            file = SFTP.open(authorized_keys2)
        else:
            print 'Choosing authorized_keys file: "',authorized_keys,'" found on the system..'
            log.write('\nChoosing authorized_keys file: "'+ authorized_keys +'" found on the system..')
            file = SFTP.open(authorized_keys)
            
        # Read non-empty lines from file
        print 'Following pub keys authorized to log in to the server: '
        log.write('\nFollowing pub keys authorized to log in to the server: \n')
        try:
            for line in file:
                if line.strip() == "":
                    continue
            else:
                    start = line.find(' ') + 1
                    end = line.find(' ', start)
                    result=line[end:].strip(" ")
                    print '\t', result,
                    log.write('\t' + result)
        finally:
            log.write('***********************\n')
            print '***********************\n'
        file.close()
        SSH.close()

    except (BadHostKeyException, AuthenticationException,SSHException, socket_error) as e:
        print "ssh fail. Authentication, BadHostKey issue, or socket error for remote", remote_host
        print '\n****************************'
        log.write('\nssh fail. Authentication, BadHostKey issue, or socket error for remote ' + remote_host)
        log.write('\n****************************') log.close()
