# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp
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

import os
import re
import time
import urllib2
import sys

def main():
    for page in range(1, 10000):
        time.sleep(1)
        searchurl = 'https://archive.org/search.php?query=collection:jamendo-albums&sort=publicdate&page=%d' % (page)
        try:
            req = urllib2.Request(searchurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
        except:
            print 'ERROR: can not download html'
            break
        
        if re.search(ur'<div class="item-ia" data-id="([^<>]+?)">', html):
            m = re.findall(ur'<div class="item-ia" data-id="([^<>]+?)">', html)
            for i in m:
                print '\n\n','#'*40,'\n',' Downloading .torrent:', i,'\n','#'*40
                torrenturl = 'https://archive.org/download/%s/%s_archive.torrent' % (i, i)
                id = int(i.split('-')[1])
                subdir = u'%.6d-%.6d' % ((id/1000)*1000, (id/1000)*1000+999)
                
                if not os.path.exists(subdir):
                    os.makedirs(subdir)
                
                downloadthis = u'wget "%s" -O "%s/%s_archive.torrent" -c' % (torrenturl, subdir, i)
                os.system(downloadthis.encode('utf-8'))
        else:
            print 'No more torrents to download'
            sys.exit()

if __name__ == '__main__':
    main()
