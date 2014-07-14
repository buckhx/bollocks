from __future__ import print_function

import os
import sys
import urllib2
import string
import textwrap

from bs4 import BeautifulSoup
from redis import Redis

URBAND_PREFIX = "urband_"

def wordgen(url):
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    popular = soup.find_all('li', class_='popular')
    for tag in popular:
        yield tag.text

def urlgen():
    urband_url = 'http://www.urbandictionary.com/popular.php?character='
    for c in string.uppercase:
        yield urband_url + c

def top():
    redis = Redis()
    words = (redis.hgetall(key) for key in redis.keys('*') if not key.startswith(URBAND_PREFIX))
    [redis.zadd('topscore', word['name'], int(word['upvote'])) for word in words]
    [redis.zadd('topdiff', word['name'], int(word['upvote'])-int(word['downvote'])) for word in words]

def show(start, count):
    redis = Redis()
    end = start+count
    words = (redis.hgetall(word) for word in redis.zrevrange('topwords', start, end))
    #words = (redis.hgetall(word) for word in redis.smembers('goodwords'))
    for word in words:
        if 'meaning' not in word or len(word['meaning']) > 360:
            continue
        print("*" * (len(word['name'])+4))
        print('* '+word['name']+' *')
        print("*" * (len(word['name'])+4))
        print("\n")
        print(textwrap.fill(word['meaning'].strip(), width=60))
        print("\n")

os.system("clear")
show(int(sys.argv[2]),int(sys.argv[1]))
