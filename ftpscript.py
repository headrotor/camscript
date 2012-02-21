#!/usr/bin/python
# hacked from http://effbot.org/librarybook/ftplib.htm
from ftplib import FTP
import os
import sys

ftp = FTP('ftp.blip.tv','username','passwd') 
print ftp.getwelcome()

fpath = os.path.normpath(sys.argv[1])
froot =  os.path.basename(fpath)

print 'opening local file' + fpath
f = open(fpath,'rb')
ftp.storbinary("STOR " + froot, f, 1024)
f.close()
data = []
ftp.dir(data.append)
for line in data:
    print "-", line
ftp.quit()
