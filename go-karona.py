#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re
import sys
import template
import requests
import json
from operator import itemgetter




def unique_path(domain,latter):
    arr=[]
    for each in latter:
        site=domain.replace('.','\.')
        pattern = '([a-zA-Z0-9\.-]*'+site+'[:0-9]{0,5})(\/[^?\s]*)(.*)?'
        st=domain+each
        result = re.findall(pattern, st)
        each=result[0][1]
        if each not in arr:
            arr.append(each)
    return arr
def sign_latter(domain,latter):
    s=""
    for each in latter:
        each=domain+each
        s=s+each+'\n'
    return s 

def execute(urls):
    hsts=""""""
    # Sorting list based on domain
    first_item = itemgetter(0)
    string = ""
    site = sys.argv[1]
    line = re.sub('\"\],?', '', urls)
    string += line

     # Domain Name
    site=site.replace('*','')
    site = re.escape(site)
    pattern = '([a-zA-Z0-9\.-]*'+site+'[:0-9]{0,5})(\/[^?\s]*)(.*)?'
    result = re.findall(pattern, string)
    new_list = sorted(result, key=first_item) # lexicographically sorted

    fin_domain=[]
    path_arr=[]

    for each in new_list:
        curren_domain=each[0]
        if curren_domain not in fin_domain:
            fin_domain.append(curren_domain)
            #print curren_domain
            #Things to do
            for each1 in new_list:
                if each1[0]==curren_domain:
                    path_arr.append(each1[1]+each1[2])
                    #Things to do
                
            hsts=hsts+build(curren_domain,path_arr)
        path_arr=[]
    return hsts

def build(domain,latter):
    html="""
    <li class="alert alert-primary" ><span><i class="icon-folder-open"></i> {}<a href="http://{}" target="_blank"> 🔗 </a></span><ul>{}</ul></li>
    """.format(domain,domain,path(domain,latter))
    return html

def path(domain,latter):
    html=""""""
    param=[]
    site=domain.replace('.','\.')
    un_path=unique_path(domain,latter)
    for each in un_path:
        each_fil=re.escape(each)
        pattern='([a-zA-Z0-9\.-]*'+site+')('+each_fil+')(.*)?'
        sp=sign_latter(domain,latter)
        result = re.findall(pattern, sp)
        for x in range(len(result)):
            param.append(result[x][2])
        current_path=each
        html=html+"""<li class="alert alert-dark"><span><i class="icon-minus-sign"></i> {}<a href="http://{}" target="_blank"> 🔗 </a></span> <ul>{}</ul></li>""".format(current_path,domain+current_path,query(domain,current_path,param))
        param=[]
    return html
          
        
def query(domain,path,param):
    html=""""""
    for each1 in param:
        html=html+"""<li class="alert alert-success"><span><i class="icon-leaf"></i>{}<a href="http://{}" target="_blank"> 🔗 </a></span> </li>""".format(domain+path+each1,domain+path+each1)
    return html




def waybackurls(hosts):
    url = 'http://web.archive.org/cdx/search/cdx?url={}/*&output=json&fl=original&collapse=urlkey'.format(hosts)
    r = requests.get(url)
    results = r.text
    return results[1:]


if __name__ == "__main__":
    print """
        
  ________                  ____  __.                                  
 /  _____/  ____           |    |/ _|____ _______  ____   ____ _____   
/   \  ___ /  _ \   ______ |      < \__  \\_  __ \/  _ \ /    \\__  \  
\    \_\  (  <_> ) /_____/ |    |  \ / __ \|  | \(  <_> )   |  \/ __ \_
 \______  /\____/          |____|__ (____  /__|   \____/|___|  (____  /
        \/                         \/    \/                  \/     \/ 

                                             https://twitter.com/kl_sree

You Got to wait.................................................

            
    """
    argc = len(sys.argv)
    if argc < 2:
        print 'Usage:\n\tpython corona.py <url> '
        sys.exit()
    host=sys.argv[1]
    urls = waybackurls(host)
    json_urls = urls
    json_urls=json_urls.strip('[\"')
    json_urls=json_urls.strip('\"],')
    if urls:        
        f = open("{}-waybackurls.html".format(host), "w")
        f.write(template.html1+execute(urls)+template.html2)
        f.close()
        print "[+]File Saved {}-waybackurls.html".format(host)
    else:
        print('[-] Found nothing')