#!/usr/bin/env python

import httplib, re
from HTMLParser import HTMLParser

countries = {}

conn = httplib.HTTPConnection("www.geonames.org")
conn.request('GET', "/countries/")
res = conn.getresponse()
if res.status == 200:
    countries.update(
        (m.group(1), m.group(5))
        for m in
        re.finditer(r'<tr><td><a name=".*"></a>(\w+)</td><td>(\w+)</td><td>(\d+)</td><td>(\w+)</td><td><a href="[^"]+">([^<]+)</a></td><td>([^<]+)</td><td class="rightalign">([0-9,.]+)</td><td class="rightalign">([0-9,.]+)</td><td>(\w+)</td></tr>', res.read()))
 
for code,name in countries.iteritems():
    print("{}={}".format(code,name))

