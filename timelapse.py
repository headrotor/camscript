#!/usr/bin/python

import sys
import os
import time
import subprocess

# make list of commands to configure cam
setup = []
setup.append("gphoto2 --set-config capture=on".split())
setup.append("gphoto2 --set-config focuslock=on".split())
setup.append("gphoto2 --set-config assistlight=0".split())
# 1024 x 768?
setup.append("gphoto2 --set-config imagesize=3".split())
# save to SRAM
setup.append("gphoto2 --set-config capturetarget=0".split())
setup.append("gphoto2 --set-config zoom=8".split())

duration_hrs = 0.25
hrs_b4_sunset = 1.5
hrs_before_sunset = 8.01
frame_delay_s = 2 
# destination directory: raw files in subdir here named by date
dest_dir = "/home/pi/cam/jpg/" 


nframes = int(duration_hrs*3600/frame_delay_s)

# first wait for hrs_before_sunset.
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
print "next sunrise"
print ephem.localtime(o.next_rising(s)).ctime()


# convert sunset time to datetime
sunset_ctime = ephem.localtime(o.next_setting(s)).ctime()
sunset_dtime = datetime.strptime(sunset_ctime, "%a %b %d %H:%M:%S %Y")
# one hour before sunset
then = sunset_dtime - timedelta(hours = hrs_before_sunset)

flag = True
while flag:
    now = datetime.now()
    print "waiting for " + str(then) + " (remaining)" +  str(then - now)
    sys.stdout.flush()
    
    if  now < then:
        time.sleep(10)
    else:
        flag = False
        
print "Done waiting, let's go!"


#http://www.moreno.marzolla.name/software/linux-time-lapse/

try:
     result = subprocess.check_output(['gphoto2', '--auto-detect'])
except subprocess.CalledProcessError:
     print "Camera not detected!"
else:
     print result
     
for cmd in setup:
     print cmd
     result = subprocess.check_output(cmd)
     print result
     time.sleep(0.5)

# make deistination directory
#datestr = time.strftime('%2y-%3j') #year followed by day in year
daystr =  time.strftime('%2y-%2m-%2d') #year followed by  mo, day
dirpath = os.path.join(dest_dir,daystr)


if not os.path.exists(dirpath):
    print "creating jpg dir " + dirpath
    os.mkdir(dirpath)


camcall = ['gphoto2', '--capture-image-and-download']
camcall.append('-I')
camcall.append('2')
camcall.append('-F')
camcall.append(str(nframes))
camcall.append('--filename')
camcall.append(os.path.join(dirpath,'%m%d%H%M%S.jpg'))
print camcall

result = subprocess.check_output(camcall)
print result

