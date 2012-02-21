#!/usr/bin/python

import sys
import os
import time
import subprocess
import fnmatch


srcfolder = os.path.normpath(sys.argv[1])
froot =  os.path.basename(srcfolder)

print "working on directory " + srcfolder
print "froot " + froot


#ffcall = "ffmpeg -r 5 -qscale 2 -i sunset2/temp%4d.jpg  -s 800x600 testsun.mp4"
ffcall = ['ffmpeg']
ffcall.append('-r')
ffcall.append('18')
ffcall.append('-qscale')
ffcall.append('2')
# doc: http://ffmpeg.org/ffmpeg.html#crop

# this crops out Sutro
#ffcall.append('-vf')
#ffcall.append('crop=800:600:650:400')

# this crops off bottom
ffcall.append('-vf')
ffcall.append('crop=in_w:1100:0:0')

# this deshakes
#x:y:w:h:rx:ry:edge:blocksize:contrast:search:filename
#ffcall.append('-vf')
#ffcall.append('deshake=-1:-1:-1:-1:16:16:0:8:100:1:shake.log,crop=800:600:650:400')

#input files
ffcall.append('-i')
ffcall.append(os.path.join(srcfolder, 'temp-%5d.jpg'))

#output file
vidfile = os.path.join('/home/jtf/cam/vid/',froot+'.mp4')
ffcall.append(vidfile)
#ffcall.append('-s')
#ffcall.append('800x600')


rmcall = ["rm"]
rmcall.append('-f')
rmcall.append(os.path.join(srcfolder,'temp*.jpg'))

#camcall = 'ls'
#camargs  = 'camraw'
print "starting movie script"

#mencoder -mc 0 -noskip -skiplimit 0 -ovc lavc -lavcopts \
#  vcodec=mpeg4:vhq:trell:mbd=2:vmax_b_frames=1:v4mv:vb_strategy=0:vlelim=0:vcelim=0:cmp=6:subcmp=6:precmp=6:predia=3:dia=3:vme=4:vqscale=1 \
#  "mf://$tmpdir/*.jpg" -mf type=jpg:fps=$fps -o $output


if True: # copy temp files

    # nuke existing temp files
    subprocess.call(rmcall)

    fnames = []
    for jfile in os.listdir(srcfolder):
        if fnmatch.fnmatch(jfile, '*.jpg'):
            fnames.append(jfile)

    fnames.sort()

    for i, f in enumerate(fnames):
        mvcall = ['cp']
        mvcall.append('-l') # make a link so we don't pound the disk
        mvcall.append(os.path.join(srcfolder,f))
        mvcall.append(os.path.join(srcfolder, "temp-%05d.jpg" % i))
        print ' '.join(mvcall)
        sys.stdout.flush()
        subprocess.call(mvcall)

# make the movie from the temp files
print ' '.join(ffcall)
subprocess.call(ffcall,stdout=sys.stdout,stderr=subprocess.STDOUT)

# and upload it
ftpcall = ['/home/jtf/cam/ftpscript.py',vidfile]
print ' '.join(ftpcall)
subprocess.call(ftpcall,stdout=sys.stdout,stderr=subprocess.STDOUT)

# now remove temp files
print ' '.join(rmcall)
subprocess.call(rmcall)    
    

    
