from dataclasses import replace
from itertools import count
from operator import contains
import requests
from bs4 import BeautifulSoup
import re

headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'}
proxylist = []
sourcefile = open("C:/Proxy-List/Sources.txt", "r")
sourcelist = sourcefile.readlines()
sourcefile.close()





#Gets HTML from specific URL
def gethtml(rawurl, headers):
    proxies = ["leer"]
    proxylist = []
    page = 0
    if "[page]" in rawurl:
#If Site has more than one pages, it will run multiple times
        while len(proxies) > 0:
            if "hidemy.name" in rawurl:
                page = page + 64
            else:
                page = page + 1
            url = rawurl.replace("[page]",f"{page}")
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            proxies =  extract(soup)
            proxylist = proxylist + proxies
            print(len(proxies), len(proxylist), url)
            
    else:
        response = requests.get(rawurl, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        proxylist = extract(soup)
    return(proxylist)


#Extracts IP:PORT from HTML but they don't need to be in the same tag
def extract(soup):
    text = soup.get_text(separator=":")
    text = text.replace("\n",":").replace(" ", "")
    while "::" in text:
        text = text.replace("::", ":")
    #print(text)
    proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    if len(proxies) < 1:
        text = f"{soup.body}"
        proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    #for proxy in proxies:
        #print(proxy)
    
    return proxies

def sort(proxylist):
    print("Sort Proxies...")
    secondproxy = ""
    proxylistnew = []
    proxylist = proxylist.sort()
    for proxy in proxylist:
        if proxy != secondproxy:
            proxylistnew = proxylistnew + proxy
        secondproxy = proxy
    return proxylistnew

def writetxt(proxylist):
    print("Writing to TXT...")
    proxytxt = '\n'.join([str(elem) for elem in proxylist])
    txt = open("./proxy.txt", "w")
    txt.write(proxytxt)
    txt.close()

#TEST
for source in sourcelist:
    rawurl = source.replace("\n", "")
    if "://" in rawurl:
        proxies = gethtml(rawurl, headers) 
        proxylist = proxylist + proxies
        print(len(proxies),len(proxylist), rawurl)
    else:
        print(source)

proxylist = sort(proxylist)

writetxt(proxylist)




#proxies = gethtml("https://proxyservers.pro/proxy/list/order/updated/order_dir/desc/page/1", headers)
#print(proxies)