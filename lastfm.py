#!/usr/bin/env python
# encoding: utf=8

import pylast
import httplib2
import simplejson as json
import urllib
import sys
import os
import re

def main(username):
  lastfm = pylast.Library(username, '6233f7e6e45ce5b642de0fca1e840032', '1c324877962f5a9a1b07097f72a4fa0d', None)
  user = lastfm.get_user()
  artists = user.get_top_artists()
  
  h = httplib2.Http(".cache")
  for artist in artists:
    try: 
      artist_name = urllib.quote_plus(artist.get_item().get_name())
      query = "http://developer.echonest.com/api/get_audio?api_key=AFB4HZSDSRBTJGC5Q&name="+artist_name+"&version=2&rows=2"
      resp, content = h.request(query, "GET")
      p = re.compile("url>(.*?)<")
      urls = p.findall(content)
      url = ""
  
      for u in urls:
        if u != None and u != '':
          url = u
  
      print "Create file for "+artist_name
      resp, content = h.request(url, "GET")
      out = open("mp3/"+artist_name+".mp3", "w")
      out.write(content)
      out.close()
      #os.system("lame -h mp3/tmp.mp3 mp3/"+artist_name+".mp3")
      #os.remove("mp3/tmp.mp3")
    except:
      print "Failed to get mp3 for "+artist_name+" from "+url

if __name__ == '__main__':
  main(sys.argv[-1])
