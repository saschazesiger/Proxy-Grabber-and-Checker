from dataclasses import replace
from itertools import count
#from operator import contains
import requests
import threading
from bs4 import BeautifulSoup
import re
import os
import shutil

#Gets HTML from specific URL
def gethtml(rawurl, log):
    proxies = ["leer"]
    proxylist = []
    page = 0
    if "[page]" in rawurl:
#If Site has more than one pages, it will run multiple times
        urlnumber = rawurl.split("]")
        urlnumber = int(urlnumber[0].replace("[", ""))
        while len(proxies) > 0:
            if "hidemy.name" in rawurl:
                page = page + 64
            else:
                page = page + 1
            if urlnumber != 0:
                urlnumber = urlnumber - 1
            else:
                print("Wiederhohlungen abgeschlossen", url)
                break
            url = rawurl.replace("[page]",f"{page}")
            url = re.sub(r"\[[0-9]+\]", "", url)
            headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            proxies =  extract(soup)
            proxylist = proxylist + proxies
    else:
        headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'}
        url = rawurl
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        proxylist = extract(soup)
    safeurl(proxylist, url)
    
    return(proxylist)

#Extracts IP:PORT from HTML but they don't need to be in the same tag
def extract(soup):
    text = soup.get_text(separator=":")
    text = text.replace("\n",":").replace(" ", "")
    while "::" in text:
        text = text.replace("::", ":")
    proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    if len(proxies) < 1:
        text = f"{soup.body}"
        proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    return proxies

#Saves Proxies to Files named after the Site the Proxy was found on
def safeurl(proxylist, url):
    proxies = '\n'.join([str(elem) for elem in proxylist])
    filename = url.split("/")
    filenameurl = filename[2]
    if filenameurl == "raw.githubusercontent.com":
        filenameurl = f"github-{filename[3]}"
    if os.path.exists(f"./raw-proxy-list/{filenameurl}.txt"):
        file = open(f"./raw-proxy-list/{filenameurl}.txt", "r")
        fileold = file.read()
        fileold = fileold.split("-----------------------------------")
        file.close()
        try:
            file = open(f"./raw-proxy-list/{filenameurl}.txt", "w")
            file.write(f"{fileold[0]}\nURL to Source: {url}\nFound Proxies: {len(proxylist)}\n-----------------------------------\n{fileold[1]}\n{proxies}")
            file.close()
        except:
            pass
    else:
        file = open(f"./raw-proxy-list/{filenameurl}.txt", "w")
        file.write(f"URL to Source: {url}\nFound Proxies: {len(proxylist)}\n-----------------------------------\n{proxies}")
        file.close()
    #print(len(proxylist), filenameurl)


#RUN
def main():
    try:
        shutil.rmtree("./raw-proxy-list/")
    except Exception as e:
        print(e)
    os.mkdir("./raw-proxy-list")
    sourcefile = open("../Sources.txt", "r")
    sourcelist = sourcefile.readlines()
    sourcefile.close()

    thread = []
    log = ""
    for source in sourcelist:
        rawurl = source.replace("\n", "")
        if "://" in rawurl:
            try:
                t = threading.Thread(target=gethtml, args=(rawurl, log))
                t.start()
                thread.append(t)
            except:
                pass

    for j in thread:
        j.join()


#RUN PROGRAMM
main()