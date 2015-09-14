# -*- coding: utf-8 -*-

# Copyright (C) 2011-2015 emijrp
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# HOWTO: python jamendo-downloader.py 0 150000
# Arguments 1 and 2 are the range of albums IDs to download (mandatory).
# As of 2015, there are about 150000 albums on Jamendo

# Argument 3 is the sound format (ogg (by default) or mp3)
# python jamendo-downloader.py 0 150000 mp3
# or python jamendo-downloader.py 0 150000 ogg
# If you want to download both formats, I recommend to create two different directories and run the script inside both

# Argument 4 is a limit for download speed in kb/s (optional). Format (number + k): 100k
# python jamendoalbums.py 0 100000 mp3 250k
# or python jamendoalbums.py 0 100000 ogg 400k

# More info (and XML database with albums metadata) http://developer.jamendo.com/en/wiki/NewDatabaseDumps

import os
import re
import time
import urllib2
import sys

def main():
    startid = 0
    endid = 150000
    sound = 'ogg2'
    speed = '10000k'

    # Your bittorrent client options (if you want to load the albums into your bittorrent)
    # Disabled with comments
    # incoming = '/media/.../Torrent'
    # incomingtorrents = '/media/.../Torrent/torrentfiles'

    if len(sys.argv) >= 2:
        startid = int(sys.argv[1])
        if startid < 0:
            print 'ERROR: id must be > 0'
            sys.exit()

    if len(sys.argv) >= 3:
        endid = int(sys.argv[2])
        if endid < 1:
            print 'ERROR: id must be > 1'
            sys.exit()

    if len(sys.argv) >= 4:
        temp = sys.argv[3].lower().strip()
        if temp == 'ogg':
            sound = 'ogg2'
        elif temp == 'mp3':
            sound = 'mp3'
        else:
            print 'ERROR: Formats allowed are ogg and mp3'
            sys.exit()

    if len(sys.argv) >= 5:
        speed = sys.argv[4]

    for id in range(startid, endid):
        print 'Trying to download album [%d]' % (id)
        time.sleep(1)
        
        urlalbum = 'https://www.jamendo.com/album/%s/' % (id)
        try:
            req = urllib2.Request(urlalbum, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            print 'ERROR: can not download html'
            break
        
        if not re.search(ur'<meta property="og:type" content="music.album" />', html):
            print 'No album [%d] available' % (id)
        else:    
            name = ''
            name = re.findall(ur'<meta property="og:title" content="([^>]+?)"\s*/>', html)[0]
            name = re.sub(ur'"', ur'\\"', name)
            
            if name:
                subdir = '%.6d-%.6d' % ((id/1000)*1000, (id/1000)*1000+999)
                prefix = '[%.6d] ' % (id)
                
                #make dir
                if not os.path.exists(subdir):
                    os.makedirs(subdir)
                
                #download .zip
                urlzip = 'https://storage.jamendo.com/download/a%d/%s/' % (id, sound)
                pathzip = subdir
                zipname = '%s%s.zip' % (prefix, name)
                os.system('wget "%s" -O "%s/%s" -c --limit-rate=%s' % (urlzip, pathzip, zipname, speed))
                time.sleep(2)            

if __name__ == '__main__':
    main()
