# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib

word = "씨발"

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

crawlingResult = open("crawlingResult.txt", "w", encoding='UTF8')

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
        crawlingResult.write(title + " ")

        #get contents
        context = m2.p.getText()
        idx = context.rfind(" - ")
        context = context.replace(" - dc official App", "")
        #print(context.strip())
        crawlingResult.write(context.strip() + "\n")

crawlingResult.close()