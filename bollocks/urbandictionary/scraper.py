import urllib2
import sys

from bs4 import BeautifulSoup

DEFINE_URL_TEMPLATE = "http://www.urbandictionary.com/define.php?term={0}"
BROWSE_URL_TEMPLATE = "http://www.urbandictionary.com/browse.php?character={0}&page={1}"

def format_key(word):
    return word.lower().replace(" ","_")

def define(word):
    url = DEFINE_URL_TEMPLATE.format(urllib2.quote(word))
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
    return lemma

def page(letter, page, popular=False):
    filters = {}
    if popular:
        filters['class'] = 'popular'
    url = BROWSE_URL_TEMPLATE.format(letter, page)
    request = urllib2.urlopen(url)
    #raise ValueError("Index too large, redirected: {0}{1}".format(letter, page))
    soup = BeautifulSoup(request.read())
    try:
        souplist = soup.find('div', {'id': 'columnist'}).ul.find_all('li', filters)
        return [word.a.text for word in souplist]
    except AttributeError, e:
        raise ValueError("Page index too large"), None, sys.exc_info()[2]

