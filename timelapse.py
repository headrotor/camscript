#!/usr/bin/python

import sys
import os
import time
import subprocess

# make list of commands to configure cam
setup = []
setup.append("gphoto2 --set-config capture=on".split())
setup.append("gphoto2 --set-config focuslock=on".split())
setup.append("gphoto2 --set-config capturetarget=0".split())
setup.append("gphoto2 --set-config zoom=8".split())
setup.append('gphoto2 --capture-image-and-download -I 2 -F 900 --filename jpg/%Y%m%d%H%M%S.jpg'.split())


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
     
exit()

# first wait for 1 hour before sunset.
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
then = sunset_dtime - timedelta(hours = 1)

flag = False
while flag:
    now = datetime.now()
    print "time before 1 hour before sunset: " +  str(then - now)
    sys.stdout.flush()
    
    if  now < then:
        time.sleep(10)
    else:
        flag = False
        
print "Almost time for sunset!"
#exit()

#Reset hub
# sudo ./usbreset /dev/bus/usb/008/004

#time.sleep(3*3600)

zoomcall = ['gphoto2','--set-config', 'Zoom=4']
print ' '.join(zoomcall)
subprocess.call(zoomcall)


camcall1 = ['gphoto2', '--capture-image-and-download']
camcall1.append('--filename')
camcall1.append('/home/jtf/cam/jpg/raw/%m%d%H%M%S.jpg')


camcall = ['gphoto2', '--capture-image-and-download']
camcall.append('--filename')

# fsize = os.path.getsize()

#camcall = 'ls'
#camargs  = 'camraw'

datestr = time.strftime('%2y-%3j') #year followed by day in year
daystr =  time.strftime('%2y-%2m-%d') #year followed by  mo, day

dirpath = "/home/pi/cam/jpg/" + datestr


print "starting cam script"

if not os.path.exists(dirpath):
    print "creating jpg dir " + dirpath
    os.mkdir(dirpath)

keepgoing = True
smallcount = 0
while(keepgoing):
    # first make filename from the current time
    fpath = dirpath + '/' + time.strftime('%2H%2M%2S') + ".jpg"
    tempcall = camcall + [fpath]
    subprocess.call(tempcall)
    print ' '.join(tempcall)
    time.sleep(1)

    # now stat the current file. If too small, then quit
    if os.path.exists(fpath):
        fsize = os.path.getsize(fpath)
        print "created %s, %d kb" % ( fpath, fsize)
        if fsize < 900000: # it's dark out
            keepgoing = False
            
#movcall = ['/home/jtf/cam/movscript.py', dirpath]
#print ' '.join(movcall)
#subprocess.call(movcall)
