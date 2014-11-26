
fh = open('/var/log/httpd/exemine_sorted', 'r')
     

prev_ip =''
tail_ip = ''
prev_time=''
tail_time = ''

count_of_equals = []
count = 0
total_equal_count = []

requested_objects = []
for line in fh:
    new_line = line.split()
    tail_ip = prev_ip
    curr_ip = new_line[1]
    prev_ip = curr_ip
    requested_obj =  (new_line[0:1] + new_line[3:])
    
    cur_itime = new_line[2]
    tail_time = prev_time
    prev_time = cur_itime

    if tail_ip == prev_ip and tail_time == prev_time:
       count += 1
       count_of_equals.append(count)
       requested_objects.append(requested_obj)
    else:
       print tail_ip, ' has done ', count, ' requests per second ', tail_time
       print '\t','Requested objects:'
       for val in requested_objects:
           print '\t', val
       requested_objects = []
       requested_objects.append(requested_obj)
       total_equal_count.append(count)
       count = 1
    
 
fh.close()

print 'Greatest amount of requests from single IP per sec is ', max(total_equal_count) 
