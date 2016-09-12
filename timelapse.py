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
# 0:3264x2448 1:2592x1944 2:2048x1536 3:1600x1200 4:640x480
setup.append("gphoto2 --set-config imagesize=3".split())
# save to SRAM
setup.append("gphoto2 --set-config capturetarget=0".split())
setup.append("gphoto2 --set-config zoom=8".split())

duration_hrs = 1.5
hrs_before_sun = 1.0
frame_delay_s = 2 
# destination directory: raw files in subdir here named by date
dest_dir = "/home/pi/cam/jpg/" 
wait_for_sun = False
sunrise = False
nframes = int(duration_hrs*3600/frame_delay_s)

if wait_for_sun:
     # first wait for hrs_before_sun.
     wait_call = ["/home/pi/gith/camscript/wait_for.py", str(hrs_before_sun)]
     if len(sys.argv) > 1:
          sunrise = True
          wait_call.append("sunrise")
          duration_hrs = 1
          hrs_before_sun = 0.25

     result = subprocess.call(wait_call)

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
if sunrise:
     daystr =  time.strftime('%2y-%2m-%2d') #year followed by  mo, day
else:
     daystr =  time.strftime('%2y-%2m-%2d-r') #year followed by  mo, day
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

