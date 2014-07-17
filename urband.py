from __future__ import print_function
from optparse import OptionParser, OptionValueError

import re
import random
import string
import util.bredis

from urbandictionary import scraper


randindex = lambda: random.choice(string.ascii_lowercase)+str(random.randint(1, 500))

def define_callback(option, opt_str, value, parser):
    try:
        defn = scraper.define(value)
        print(defn['name']+':'+defn['meaning'])
    except ValueError:
        raise OptionValueError("Cannot find definiton for: "+value)

def page_callback(option, opt_str, index, parser):
    print(50*"*")
    print("Paging urband...")
    if "random"[:len(index.lower())] == index.lower():
        index = None
        while index is None:
            index = randindex()
            print("Rolling: "+index)
            try:
                scraper.page(index[0], index[1:])
            except ValueError:
                print(index+" out of bounds, rerolling...")
                index = None
    if not re.match("^[a-zA-Z][0-9]+$", index):
        raise OptionValueError("Page Index must be of form <LETTER><NUMBER> ie. R31. Value was: "+index)
    letter, page = index[0], index[1:]
    print("Looking up page: "+index)
    print(50*"*")
    try:
        [print(word) for word in scraper.page(letter, page)]
    except ValueError:
       raise OptionValueError("Page index out of range: "+index)

def slurp_callback(option, opt_str, value, parser):
    try:
        defn = scraper.define(value)
        if len(parser.rargs) > 0 and not parser.rargs[0].startswith('-'):
            defn["meaning"] = parser.rargs[0]
            del parser.rargs[0]
        util.bredis.slurp(defn)
        key = util.bredis.defn_key(value)
        print("Slurped {0} with key: {1}".format(value, key))
    except ValueError:
        raise OptionValueError("Cannot find definiton for: "+value)

optparser = OptionParser()

optparser.add_option('-d', '--define', dest="define", type='str',
    action="callback", callback=define_callback,
    metavar="HEADWORD", help="Look up definition to HEADWORD")

optparser.add_option('-p', '--page', dest="page", type='str',
    action="callback", callback=page_callback,
    metavar="INDEX", help="List entries at index. Index is in the form <LETTER><NUMBER>. B52 is page 52 of B entries. 'random' will pick a random index")

optparser.add_option('-s', '--slurp', dest="slurp", type='str',
    action="callback", callback=slurp_callback,
    metavar="HEADWORD", help="Slurp HEADWORD into bredis with definition and other attributes")

(opts, args) = optparser.parse_args()
