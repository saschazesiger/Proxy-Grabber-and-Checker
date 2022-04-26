from email import charset
from selenium import webdriver #pip install selenium
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import threading
import requests

url = 'https://advanced.name/freeproxy?page=1'


def getrooturl(url):
    if "raw.githubusercontent.com" in url:
        root = "github-"+url.split("/")[3]
    else:
        root = url.split("/")[2].replace("www.", "")
    return root

def gethtmljs(url, log):
    proxies = []
    if "[page]" in url:
        num = url.split("]")
        num = int(num[0].replace("[", ""))
        denum = num
        clock = 0
        while num > 0:
            newproxies = []
            clock = clock + 1
            num = num - 1
            newurl = url.replace("[page]", f"{clock}").replace(f"[{denum}]", "")
            html = gethtmljsraw(newurl)
            newproxies = extract(html)
            proxies.extend(newproxies)
            if len(newproxies) < 1:
                break
    else:
        html = gethtmljsraw(url)
        proxies = extract(html)
    rooturl = getrooturl(url)
    proxylist =  '\n'.join([str(elem) for elem in proxies])
    with open("./raw.txt", "a") as f:
        f.write(f"{proxylist}\n")
    with open("./provider.csv", "a") as f:
        f.write(f"{rooturl};{len(proxies)}\n")
    return proxies

def gethtmljsraw(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("window-size=600,600")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--log-level=3")
    driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html

def gethtml(url, log):
    proxies = []
    if "[page]" in url:
        num = url.split("]")
        num = int(num[0].replace("[", ""))
        denum = num
        clock = 0
        while num > 0:
            newproxies = []
            if "hidemy.name" in url:
                clock = clock + 64
            else:
                clock = clock + 1
            num = num - 1
            newurl = url.replace("[page]", f"{clock}").replace(f"[{denum}]", "")
            html = gethtmlraw(newurl)
            newproxies = extract(html)
            proxies.extend(newproxies)
            if len(newproxies) < 1:
                break      
    else:
        html = gethtmlraw(url)
        proxies = extract(html)
    rooturl = getrooturl(url)
    proxylist =  '\n'.join([str(elem) for elem in proxies])
    with open("./raw.txt", "a") as f:
        f.write(f"{proxylist}\n")
    with open("./provider.csv", "a") as f:
        f.write(f"{rooturl};{len(proxies)}\n")
    return proxies

def gethtmlraw(url):
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'}
    response = requests.get(url, headers=headers, timeout=30)
    html = response.content
    return html

def extract(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text(separator=":")
    text = text.replace("\n",":").replace(" ", "")
    while "::" in text:
        text = text.replace("::", ":")
    proxies = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\:\d{1,5}\b", text)
    return proxies

def normalizer():
    with open("./raw.txt", "r") as f:
        proxies = f.readlines()
    proxies.sort()
    before = ""
    proxiesdup = ""
    all = 0
    nodups = 0
    for proxy in proxies:
        all = all + 1
        if proxy != before:
            proxiesdup = proxiesdup + proxy
            nodups = nodups + 1
        before = proxy

    with open("./provider.csv", "a") as f:
        f.write(f"All: {all}, Without Duplicates: {nodups}")
    with open("./all.txt", "w") as f:
        f.write(proxiesdup)


def start():
    with open("./sources.txt", "r") as f:
        sources = f.readlines()
    with open("./raw.txt", "w") as f:
        f.write("")
    with open("./provider.csv", "w") as f:
        f.write("")
    thread = []
    log = ""
    for source in sources:
        rawurl = source.replace("\n", "")
        if "://" in rawurl:
            if "[js]" in rawurl:
                rawurl = rawurl.replace("[js]", "")
                t = threading.Thread(target=gethtmljs, args=(rawurl, log))
                t.start()
                thread.append(t)
            else:
                t = threading.Thread(target=gethtml, args=(rawurl, log))
                t.start()
                thread.append(t)
    for j in thread:
        j.join() 
    normalizer()
    print("Finish")

start()