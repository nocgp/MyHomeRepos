import paramiko, platform
from paramiko.ssh_exception import SSHException, BadHostKeyException, AuthenticationException
from socket import error as socket_error

localpath ='/tmp/os_name.py'
remotepath ='/tmp/os_name.py'
host= ['','']


for value in host:
     try:
        SSH = paramiko.SSHClient()
        SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        SSH.connect(value)
        print '--------------------------------------------'
	print "Checking : ", value       
        SFTP = SSH.open_sftp()
        SFTP.put(localpath,remotepath)
        i, o, e = SSH.exec_command("python /tmp/os_name.py")
	s = e.read()
	if s: 					# an error occurred
    		print s
	else:
		print o.read()
        
	
	SSH.close()

     except (BadHostKeyException, AuthenticationException,SSHException, socket_error) as e:
        print "ssh fail. Authentication, BadHostKey issue, or socket error for remote", value


