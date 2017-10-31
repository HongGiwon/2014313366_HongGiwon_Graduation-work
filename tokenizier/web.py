# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re

p = re.compile("[\u0000-\u001f\u0020\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff]")

def string_re(inputstring):
    m = p.findall(inputstring)
    return ("".join(m))

words = open("badwords.txt","r").read().splitlines()
count = 78

for word in words :
    param = urllib.parse.quote(word).replace("%", ".")

    urlfront = 'http://search.dcinside.com'
    url = 'http://search.dcinside.com/post/q/' + param
    urlback = "/q/" + param
    #print(url)

    data = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(data, "lxml")

    link = soup.find_all("div", {"class": "thumb_txt"})

    link2 = soup.find('div', {"id": "dgn_btn_paging"}).findAll('a', href=True)
    #print(link2[-1]["href"])
    #print(link2[-1]["href"][8:10].replace("/", ""))
    lastPage = int(link2[-1]["href"][8:10].replace("/", ""))

    print("word: " + word)
    print("pages: 1 ~ " + str(lastPage))

    count = count + 1
    crawlingResult = open("crawlingResult" + str(count) + ".txt", "w", encoding='UTF8')

    for i in range(1, lastPage + 1):
        pageUrl = urlfront+"/post/p/" + str(i) + urlback
        print(str(i) + ": " + pageUrl)
        pageData = urllib.request.urlopen(pageUrl).read()
        link3 = BeautifulSoup(pageData, "lxml").find_all("div", {"class": "thumb_txt"})
        for m2 in link3:
            #get title
            title = m2.a.get_text()
            idx = title.rfind(" - ")
            title = title[0:idx]
            #print(title)
            crawlingResult.write(string_re(title) + " ")

            #get contents
            context = m2.p.getText()
            idx = context.rfind(" - ")
            context = context.replace(" - dc official App", "")
            #print(context.strip())
            crawlingResult.write(string_re(context).strip() + "\n")

    crawlingResult.close()