#!/usr/bin/python

import sys
import os
import time
import subprocess

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

dirpath = "/home/jtf/cam/jpg/" + datestr


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
            
movcall = ['/home/jtf/cam/movscript.py', dirpath]
print ' '.join(movcall)
subprocess.call(movcall)
