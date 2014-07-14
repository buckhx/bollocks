from __future__ import print_function
from optparse import OptionParser, OptionValueError

import re
import random
import string

from urbandictionary import scraper

randindex = lambda: random.choice(string.ascii_lowercase)+str(random.randint(1, 500))

def define_callback(option, opt_str, value, parser):
    defn = scraper.define(value)
    print(defn['name']+':'+defn['meaning'])

def page_callback(option, opt_str, index, parser):
    if "random"[:len(index.lower())] == index.lower():
        index = None
        while index is None:
            index = randindex()
            try:
                scraper.page(index[0], index[1:])
            except ValueError:
                print(index+" out of bounds, rerolling...")
                index = None
    if not re.match("^[a-zA-Z][0-9]+$", index):
        raise OptionValueError("Page Index must be of form <LETTER><NUMBER> ie. R31. Value was: "+index)
    letter, page = index[0], index[1:]
    try:
        [print(word) for word in scraper.page(letter, page)]
    except ValueError:
       raise OptionValueError("Page index out of range: "+index)

optparser = OptionParser()

optparser.add_option('-d', '--define', dest="define", type='str',
    action="callback", callback=define_callback,
    metavar="HEADWORD", help="Look up definition to HEADWORD")

optparser.add_option('-p', '--page', dest="page", type='str',
    action="callback", callback=page_callback,
    metavar="INDEX", help="List entries at index. Index is in the form <LETTER><NUMBER>. B52 is page 52 of B entries. 'random' will pick a random index")

(opts, args) = optparser.parse_args()
