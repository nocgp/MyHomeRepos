import platform,subprocess

cut_string = platform.platform().split('with-')
new_string = cut_string[1]

print 
print 'node     :', platform.node()
print 'system   :', platform.system()
print 'release  :', platform.release()
print 'platform :', new_string
print 'processor:', platform.processor()
print 'Updates:'

p = subprocess.Popen(["yum", "list", "updates"], stdout=subprocess.PIPE, bufsize=1)
for line in p.stdout:
    print line.rstrip("\n")
p.wait()
print '--------------------------------------------'
