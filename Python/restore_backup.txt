#!/bin/env python
""" 
Please note that this is customer specific
	Usage:
see available dumps: --user longisland --host XX
restore from dump: --user longisland --host XX --backup_time old(current) --backup_name file_name
"""
import sys,re,time
import paramiko
from paramiko.ssh_exception import SSHException, BadHostKeyException, AuthenticationException
from socket import error as socket_error
import optparse, commands, pexpect

usage = "usage: %prog --user XX --host XX --backup_time XX --backup_name XX"
parser = optparse.OptionParser(usage)
parser.add_option('--user', action="store", type="str", help='user name from PCadmins')
parser.add_option('--host', action="store", type="str", help='server name from PCadmins')
parser.add_option('--backup_time', action="store", type="str", help='folder name from where restart: current, old, very_old, etc')
parser.add_option('--backup_name', action="store", type="str", help='backup file name that needs to be restored')
parser.add_option('--backup_path', action="store", type="str", help='backup path: copy past it from the screen')
(options, args) = parser.parse_args()

if len(sys.argv) == 1:
   sys.exit("No arguments were given. Please refer to help: restore_backup.py --help")

backup_server = 'backup.server.com'
openbizbox_install = '/home/' + options.user + '/configs/openbizbox_install.info'
openbizbox_content = ''
db = ''
current_dump = ''
old_dump = ''
very_old_dump = ''
host_name = ''
daily_1 = ''
daily_2 = ''
daily_3 = ''
daily_4 = ''
daily_5 = ''
daily_6 = ''
weekly_1 = ''
weekly_2 = ''
weekly_3 = ''
monthly_1 = ''
monthly_2 = ''

def db_name_searcher(text):
        db_name_matched = re.search('DB_NAME=', text)
	if db_name_matched: return text
	else: return False

# Read shop config and find db_name there 
try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(options.host)
        stdin, stdout, stderr = ssh.exec_command("cat " + openbizbox_install)
        openbizbox_content = stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command("hostname -f")
        for line in stdout.readlines():
            new_line = line.split() 
            host_name = new_line[0]
        ssh.close()
except (BadHostKeyException, AuthenticationException,SSHException, socket_error) as e:
        print "ssh fail ", options.host

for line in openbizbox_content:
    db_matched = db_name_searcher(line)
    if db_matched:
       db_name = db_matched.split('=')[1].replace('\n','').split('"')
       db = db_name[1]

# list of current, old dumps for given user
try:
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(backup_server)
	stdin, stdout, stderr = ssh.exec_command("ls -lht /mnt/backup/db/mysql/" + db + "/current/")
	current_dump = stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command("ls -lht /mnt/backup/db/mysql/" + db + "/old/")
        old_dump = stdout.readlines()
        stdin, stdout, stderr = ssh.exec_command("ls -lht /mnt/backup/db/mysql/" + db + "/very_old/")
        very_old_dump = stdout.readlines()
        stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.1/sqldump/" + db + ".sql.gz")
        if stderr.readlines():
		pass
        else:
        	daily_1 = stdout.readlines()
	        stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.2/sqldump/"+ db + ".sql.gz")
        	daily_2 = stdout.readlines() 
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.3/sqldump/"+ db + ".sql.gz")
	        daily_3 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.4/sqldump/"+ db + ".sql.gz")
	        daily_4 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.5/sqldump/"+ db + ".sql.gz")
        	daily_5 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/daily.6/sqldump/"+ db + ".sql.gz") 
	        daily_6 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/weekly.1/sqldump/"+ db + ".sql.gz")
		weekly_1 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/weekly.2/sqldump/"+ db + ".sql.gz")
		weekly_2 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/weekly.3/sqldump/"+ db + ".sql.gz")
		weekly_3 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/monthly.1/sqldump/"+ db + ".sql.gz")
		monthly_1 = stdout.readlines()
		stdin, stdout,stderr = ssh.exec_command("ls -lht /mnt/backup/db/" + host_name + "/var/backups/mysql/monthly.2/sqldump/"+ db + ".sql.gz")
		monthly_2 = stdout.readlines()
	ssh.close()
except (BadHostKeyException, AuthenticationException,SSHException, socket_error) as e:
       	print "ssh fail ", backup_server

print '\nAvailable dumps are:\n'
print '-------------- '
if len(current_dump)>0:
   print ("Current dump for given user in " + backup_server + ":/mnt/backup/db/mysql/" + db + "/current/")
   for line in current_dump[1:]:
       print '\t',line, 
else: print ("Current dump is not found on backup server: " + backup_server + ":/mnt/backup/db/mysql/" + db + "/current/")
print '-------------- '
if len(old_dump)>0:
   print ("Old dump found for given user in " + backup_server + ":/mnt/backup/db/mysql/" + db + "/old/")
   for  line in old_dump[1:]:
        print '\t',line,
else: print ("Old dump is not found on backup server: " + backup_server + ":/mnt/backup/db/mysql/" + db + "/old/")
print '-------------- '
if len(very_old_dump)>0:
   print ("Very old dump found for given user in " + backup_server + ":/mnt/backup/db/mysql/" + db + "/very_old/")
   for  line in very_old_dump[1:]:
        print '\t',line,
else: print ("Very old dump is not found on backup server: " + backup_server + ":/mnt/backup/db/mysql/" + db + "/very_old/")

if len(daily_1)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.1/sqldump/"+ db + ".sql.gz")
   for  line in daily_1:
        print '\t',line,
if len(daily_2)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.2/sqldump/"+ db + ".sql.gz")
   for  line in daily_2:
        print '\t',line,
if len(daily_3)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.3/sqldump/"+ db + ".sql.gz")
   for  line in daily_3:
        print '\t',line,
if len(daily_4)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.4/sqldump/"+ db + ".sql.gz")
   for  line in daily_4:
        print '\t',line,
if len(daily_5)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.5/sqldump/"+ db + ".sql.gz")
   for  line in daily_5:
        print '\t',line,
if len(daily_6)>0:
   print '-------------- '
   print ("Daily dump found " + backup_server + ":/var/backups/mysql/daily.6/sqldump/"+ db + ".sql.gz")
   for  line in daily_6:
        print '\t',line,
if len(weekly_1)>0:
   print '-------------- '
   print ("Weekly dump found " + backup_server + ":/var/backups/mysql/weekly.1/sqldump/"+ db + ".sql.gz")
   for  line in weekly_1:
        print '\t',line,
if len(weekly_2)>0:
   print '-------------- '
   print ("Weekly dump found " + backup_server + ":/var/backups/mysql/weekly.2/sqldump/"+ db + ".sql.gz")
   for  line in weekly_2:
        print '\t',line,
if len(weekly_3)>0:
   print '-------------- '
   print ("Weekly dump found " + backup_server + ":/var/backups/mysql/weekly.3/sqldump/"+ db + ".sql.gz")
   for  line in weekly_3:
        print '\t',line,
if len(monthly_1)>0:
   print '-------------- '
   print ("Monthly dump found " + backup_server + ":/var/backups/mysql/monthly.1/sqldump/"+ db + ".sql.gz")
   for  line in monthly_1:
        print '\t',line,
if len(monthly_2)>0:
   print '-------------- '
   print ("Monthly dump found " + backup_server + ":/var/backups/mysql/monthly.2/sqldump/"+ db + ".sql.gz")
   for  line in monthly_2:
        print '\t',line,


print '\nTo restore database:\n1. run script as: restore_backup.py --user USER --host HOST --backup_path BACKUP_PATH\n2. OR run as:  restore_backup.py --user USER --host HOST --backup_time current(old,etc) --backup_name FILE_NAME_TO_restore'
print 'Examples:\n1. restore_backup.py --user htz21 --host SERVER-PC --backup_path /mnt/backup/db/SERVER-PC/var/backups/mysql/weekly.3/sqldump/db.sql.gz'
print '2. restore_backup.py --user htz21 --host SERVER-PC --backup_time current --backup_name db.mysql.gz'
# Restore backup if options were given
if (options.backup_time) and (options.backup_name):
     print '\n--------------'
     print 'Retoring process started.....'
     restore_from = "/mnt/backup/db/mysql/" + db + "/" + options.backup_time + "/" + options.backup_name
     print ('Backup will be restored from ' + backup_server +':' + restore_from)
     time.sleep(5)
     command = "scp " + backup_server + ":" + restore_from + " " + options.host + ":/home/" + options.user + "/"
     ssh_newkey = 'Are you sure you want to continue connecting'
     p=pexpect.spawn(command)
     server_answers = p.expect([ssh_newkey, 'password:', pexpect.EOF])
     if server_answers == 0:
    	print "I say yes"
    	p.sendline('yes')
    	server_answers = p.expect(['password:', pexpect.EOF])
     if server_answers == 1:
    	print "I give password",
	p.sendline("mypassword")
	p.expect(pexpect.EOF)
     elif server_answers == 2:
    	print 'Copy dump to destination server process bar: '
    	pass
     print p.before
     # Dump current and restore old
     ssh = paramiko.SSHClient()
     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     ssh.connect(options.host)
     (stdin, stdout, stderr) = ssh.exec_command("/usr/bin/mysqldump " + db + " > /root/" + db + ".mysql")
     stdout = stdout.readlines()
     stderr  = stderr.readlines()
     if stdout:
        print stdout
     elif stderr:
        print stderr
        sys.exit("Error dumping current database. Fix an error and run script again with the same options")
     else:
        (stdin, stdout, stderr) = ssh.exec_command("ls -lht /root/" + db + ".mysql")
        print '\nCurrent database dumped : '
        for line in  stdout.readlines():
            print line,
        (stdin, stdout, stderr) = ssh.exec_command("tail -1 /root/" + db + ".mysql")
        for line in  stdout.readlines():
            print line,
        time.sleep(5)
        print ("Restoring from copied dump: /home/" + options.user + "/"+ options.backup_name)
        print 'You will have 20 sec now to cancell this job..'
        time.sleep(20)
        print 'Restoring..'
        (stdin, stdout, stderr) = ssh.exec_command("gunzip < " + "/home/" + options.user + "/"+ options.backup_name  + " | mysql " + db)
        if stdout.readlines():
           for line in stdout.readlines():
               print line,
        elif stderr.readlines():
           for line in stderr.readlines():
               print line,
        else:
           print ('Dump restored succesfully.\nJist in case reset OBB cache on ' + options.host + ' with command: /usr/share/obbdeploy/manager.php --task=set-permissions --user='+db+'-www')
     ssh.close()
elif options.backup_path:
     print '\n--------------'
     print 'Retoring process started.....'
     restore_from = options.backup_path
     print ('Backup will be restored from ' + backup_server +':' + restore_from)
     time.sleep(5)
     command = "scp " + backup_server + ":" + restore_from + " " + options.host + ":/home/" + options.user + "/"
     ssh_newkey = 'Are you sure you want to continue connecting'
     p=pexpect.spawn(command)
     server_answers = p.expect([ssh_newkey, 'password:', pexpect.EOF])
     if server_answers == 0:
        print "I say yes"
        p.sendline('yes')
        server_answers = p.expect(['password:', pexpect.EOF])
     if server_answers == 1:
        print "I give password",
        p.sendline("mypassword")
        p.expect(pexpect.EOF)
     elif server_answers == 2:
        print 'Copy dump to destination server process bar: '
        pass
     print p.before
     # Dump current and restore old
     ssh = paramiko.SSHClient()
     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
     ssh.connect(options.host)
     (stdin, stdout, stderr) = ssh.exec_command("/usr/bin/mysqldump " + db + " > /root/" + db + ".mysql")
     stdout = stdout.readlines()
     stderr  = stderr.readlines()
     if stdout:
        print stdout
     elif stderr:
        print stderr
        sys.exit("Error dumping current database. Fix an error and run script again with the same options")
     else:
        (stdin, stdout, stderr) = ssh.exec_command("ls -lht /root/" + db + ".mysql")
        print '\nCurrent database dumped : '
        for line in  stdout.readlines():
            print line,
        (stdin, stdout, stderr) = ssh.exec_command("tail -1 /root/" + db + ".mysql")
        for line in  stdout.readlines():
            print line,
        time.sleep(5)
        print ("Restoring from copied dump: /home/" + options.user + "/"+ db + ".sql.gz")
        print 'You will have 20 sec now to cancell this job..'
        time.sleep(20)
        print 'Restoring..'
        (stdin, stdout, stderr) = ssh.exec_command("gunzip < " + "/home/" + options.user + "/"+ db + ".sql.gz"  + " | mysql " + db)
        if stdout.readlines():
           for line in stdout.readlines():
               print line,
        elif stderr.readlines():
           for line in stderr.readlines():
               print line,
	else:
           print ('Dump restored succesfully.\nJist in case reset OBB cache on ' + options.host + ' with command: /usr/share/obbdeploy/manager.php --task=set-permissions --user='+db+'-www')
     ssh.close()
