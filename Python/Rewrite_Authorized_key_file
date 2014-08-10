# Script reads /root/.ssh/authorized_keys or /root/.ssh/authorized_keys2
# Makes backup of above file to /root/.ssh/trash dir
# Removes all matches found
# Logs all it does to /tmp/authorized_keys_log_file on the server from where you started the script
# How to Run
#    copy file to admindesk.gpserver.dk to /tmp
#    define variables below
#    start script as: python script_name
import paramiko, time, os, re
from paramiko.ssh_exception import SSHException, BadHostKeyException, AuthenticationException
from socket import error as socket_error

#### Please define these variables below.
backup_dir = '/root/.ssh/trash'
authorized_keys = '/root/.ssh/authorized_keys'
authorized_keys2 = '/root/.ssh/authorized_keys2'
log_file = '/tmp/authorized_keys_log_file_REWTITTEN'

host_list = ['hosts', 'list']

regexes=['strings', 'list']
################################################

def remote_file_does_not_exist(sftp, file_to_check):
  try: sftp.stat(file_to_check)
  except (IOError) as e:
      if e[0] == 2: return True
      else: return False

def remote_backup_dir_does_not_exist(sftp, dir_to_check):
  try: sftp.stat(dir_to_check)
  except (IOError) as e:
      if e[0] == 2: return True
      else: return False

def do_backup_of_file(file_to_backup, backup_dir, ssh):
  path, file_name = os.path.split(file_to_backup)
  ssh.exec_command('cp' +' '+ file_to_backup + ' ' + backup_dir + '/'
                   + file_name + '.' + time.strftime("%Y-%m-%d-%H_%M_%S"))

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

      # Check and create, if needed, backup dir
      if remote_backup_dir_does_not_exist(SFTP, backup_dir):
          print 'Checking backup dir: "',backup_dir,'" does not exist.. Creating dir: mkdir',backup_dir
          log.write('\nChecking backup dir: "'+ backup_dir +'" does not exist.. Creating dir: mkdir ' + backup_dir)
          SFTP.mkdir(backup_dir)
      else:
          print 'Checking backup dir: "', backup_dir, '" exists on the system..'
          log.write('\nChecking backup dir: "'+ backup_dir +'" exists on the system..')

      # Choose and backup authorized_keys/authorized_keys2
      if remote_file_does_not_exist(SFTP, authorized_keys):
          print 'Choosing authorized_keys file: "', authorized_keys, '" does not exist.. Open "',authorized_keys2,'"'
          log.write('\nChoosing authorized_keys file: "' + authorized_keys + '" does not exist.. Open "'
                    + authorized_keys2 + '"')
          file = SFTP.open(authorized_keys2)
          print 'Doing backup of: "',authorized_keys2,'"'
          log.write('\nDoing backup of: "'+ authorized_keys2 +'"')
          do_backup_of_file(authorized_keys2, backup_dir, SSH)
      else:
          print 'Choosing authorized_keys file: "',authorized_keys,'" found on the system..'
          log.write('\nChoosing authorized_keys file: "'+ authorized_keys +'" found on the system..')
          file = SFTP.open(authorized_keys)
          print 'Doing backup of: "', authorized_keys,'"'
          log.write('\nDoing backup of: "'+authorized_keys +'"')
          do_backup_of_file(authorized_keys, backup_dir, SSH)

      # Read non-empty lines from file
      print 'Reading the file, scan matches..\n'
      log.write('\nReading the file, scan  matches..\n')
      r=re.compile('|'.join(regexes))
      new_content=[]
      matches = False
      for line in file:
          if line.strip() == "":
                  continue
          else:
              start = line.find(' ') + 1
              end = line.find(' ', start)
              if r.search(line):
                  matches = True
                  print 'Matches found in \t',line[end:].strip(" ")
                  log.write('\nMatches found in\t' + line[end:].strip(" "))
              else:
                  new_content.append(line) 
      file.close()
      
      if matches:
          print "Starting to rewrite the file..\n"
          log.write("\nStarting to rewrite the file..\n")
          if remote_file_does_not_exist(SFTP, authorized_keys):
              file_to_rewrite = SFTP.open(authorized_keys2,'w')
          else:
              file_to_rewrite = SFTP.open(authorized_keys, 'w')
          
          for li in new_content:
              file_to_rewrite.write(li.strip() + '\n')
          file_to_rewrite.close
      else:
          print "\tNothing to rewrite..\n"
          print "*****************************\n"
          log.write("\tNothing to rewrite..\n") 
          log.write("*****************************\n")        
      SSH.close()

  except (BadHostKeyException, AuthenticationException,SSHException, socket_error) as e:
      print "ssh fail. Authentication, BadHostKey issue, or socket error for remote", remote_host
      print "\n*****************************"
      log.write('\nssh fail. Authentication, BadHostKey issue, or socket error for remote ' + remote_host)
      log.write("\n*****************************") 
log.close()
