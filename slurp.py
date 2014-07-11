import sys
import urllib2

from bs4 import BeautifulSoup

BASE_URL = "http://www.urbandictionary.com/define.php?term="

def format_key(word):
    return word.lower().replace(" ","_")

def slurp(word):
    url = BASE_URL+urllib2.quote(word)
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    box = soup.find(class_="box")
    key = format_key(word)
    lemma = {}
    lemma['name'] = box.find(class_="word").a.text
    lemma['meaning'] = box.find(class_="meaning").text
    lemma['defid'] = box.attrs['data-defid']
    lemma['contributor'] = str(box.find(class_="contributor"))
    lemma['example'] = box.find(class_="example").text
    lemma['upvote'] = box.find(class_="up").span.text
    lemma['downvote'] = box.find(class_="down").span.text
    #redis.hput(key, lemma)
    #redis.hput(goodwords)
    print key+": "+lemma['meaning']

slurp(sys.argv[1])

