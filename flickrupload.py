import flickrapi as f
import subprocess
import xml
import sys
import os

# file to upload
fname = sys.argv[1]

# get flickr credentials from file
creds = subprocess.check_output(['cat', 'flickr_cred.txt'])
user, api_key, api_secret = creds.split()



flickr = f.FlickrAPI(api_key, api_secret)
(token, frob) = flickr.get_token_part_one(perms='write')
if not token:
        raw_input("Press ENTER after you authorized this program")
flickr.get_token_part_two((token, frob))

result = flickr.upload(fname, title=fname, tags='sunset timelapse "San Francisco"') 
xml.etree.ElementTree.dump(result)

exit()

try :
    username = sys.argv[1]
    photoset_idx = int(sys.argv[2])
    try :
        access_token = sys.argv[3]
        f.set_auth_handler(access_token)
    except IndexError : pass
    u = f.Person.findByUserName(username)
    ps = u.getPhotosets()[photoset_idx]
    
    if not os.path.exists(ps.title) : os.mkdir(ps.title)
    os.chdir(ps.title)
    
    for p in ps.getPhotos() :
        p.save(p.title+".jpg")
except IndexError :
    print "usage: python download_album.py username album_idx [access_token_file]"
    print "Downloads the content of a user's album."
    print "'album_idx' stands of the album index as given by the 'show_albums.py'"
    print "script. A new directory with the album title will be created and the"
    print "album content will be downloaded in this directory."




                                    
