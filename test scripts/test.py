from dataclasses import replace
from itertools import count
from operator import contains
import requests
from bs4 import BeautifulSoup
import re

rawurl = "https://premproxy.com/list/0[page].htm"
headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'}


#Gets HTML from specific URL
def gethtml(rawurl, headers):
    proxies = ["leer"]
    page = 0
    if "[page]" in rawurl:
#If Site has more than one pages, it will run multiple times
        while len(proxies) > 0:
            if "hidemy.name" in rawurl:
                page = page + 64
            else:
                page = page + 1
            url = rawurl.replace("[page]",f"{page}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            proxies = extract2(soup)
            print(len(proxies), page)
    else:
        response = requests.get(rawurl, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        

        proxies = extract2(soup)
        print(len(proxies))

#Extracts IP:PORT from HTML
def extract1(soup):
    text = f"{soup.body}"
    proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    return proxies

#Extracts IP:PORT from HTML but they don't need to be in the same tag
def extract2(soup):
    text = soup.get_text(separator=":")
    text = text.replace("\n",":").replace("::",":").replace("::",":")
    #print(text)
    proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    return proxies



#TEST
gethtml(rawurl, headers)