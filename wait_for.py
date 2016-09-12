#!/usr/bin/python
import sys
import os
import time

def print_usage():
    print """ Usage: python wait_for.py <hours_before> <sunrise>"""
    print """  <hours_before> float hourse before event"""
    print """  <sunrise> any string indicates sunrise, OW sunset"""
    exit()

if len(sys.argv) < 2:
    print_usage()

try:
    hrs_before = float(sys.argv[1])
except:
    print_usage()
    
if len(sys.argv) == 3:
    sunrise = True
else:
    sunrise = False


#Calculate sunset
import ephem
from datetime import datetime, timedelta
import time
o=ephem.Observer()
o.lat='37.7749'
o.long='-122.4194'
s=ephem.Sun()
#s=ephem.Moon()
s.compute()

# convert sun event time to datetime
if sunrise:
    event_ctime = ephem.localtime(o.next_rising(s)).ctime()

else:
    event_ctime = ephem.localtime(o.next_setting(s)).ctime()
    
event_dtime = datetime.strptime(event_ctime, "%a %b %d %H:%M:%S %Y")

# time before event
then = event_dtime - timedelta(hours = hrs_before)

flag = True
if sunrise:
    print("wait for {:f} hours before sunrise".format(hrs_before))
else:
     print("wait for {:f} hours before sunset".format(hrs_before))
sys.stdout.flush()
    
while flag:
    now = datetime.now()
    print "waiting for " + str(then) + " (remaining)" +  str(then - now)
    sys.stdout.flush()
    
    if  now < then:
        time.sleep(10)
    else:
        flag = False
        
print "Done waiting, let's go!"

