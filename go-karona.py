#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import sys
import requests
import template
import json

def waybackurls(hosts):
    url = 'http://web.archive.org/cdx/search/cdx?url={}/*&output=json&fl=original&collapse=urlkey'.format(hosts)
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    }
    r = requests.get(url,headers=headers)
    results = r.text
    return results[1:]

def sortit(urls):
    dicton={}
    site = sys.argv[1]
    site=site.replace('*','')
    site = re.escape(site)
    pattern = '(http[s]?://[a-zA-Z0-9\.-]*'+site+'[:0-9]{0,5})(\/[^?\s]*)(.*)?'
    result = re.findall(pattern, urls)
    for each in result:
        if str(each[0]) not in dicton:
            dt={"":[""]}
            dicton[str(each[0])]=dt
        if str(each[1]) not in dicton[str(each[0])]:
            dicton[str(each[0])][str(each[1])]=[]
        if str(each[2]) not in dicton[str(each[0])][str(each[1])]:
            dicton[str(each[0])][str(each[1])].append(str(each[2]))
    return json.dumps(dicton, sort_keys = True)


if __name__ == "__main__":
    print """
        
  ________                  ____  __.                                  
 /  _____/  ____           |    |/ _|____ _______  ____   ____ _____   
/   \  ___ /  _ \   ______ |      < \__  \\_  __ \/  _ \ /    \\__  \  
\    \_\  (  <_> ) /_____/ |    |  \ / __ \|  | \(  <_> )   |  \/ __ \_
 \______  /\____/          |____|__ (____  /__|   \____/|___|  (____  /
        \/                         \/    \/                  \/     \/ 

                                             https://twitter.com/kl_sree

...........................................................................

            
    """
    argc = len(sys.argv)
    if argc < 2:
        print 'Usage:\n\tpython go-karona.py <url> '
        sys.exit()
    host=sys.argv[1]
    urls = waybackurls(host)
    pattern='(\[\"|\"\]\,?\]?)'
    urls=re.sub(pattern, '', urls)
    if urls:
        jval=sortit(urls)
        f = open("{}.js".format(host), "w")
        f.write("var data="+jval)
        f = open("{}-waybackurls.html".format(host), "w")
        f.write(template.html1+"<script src='{}.js'></script>".format(host)+template.html2)
        print "[+]File Saved {}-waybackurls.html".format(host)
    else:
        print('[-] Found nothing')
