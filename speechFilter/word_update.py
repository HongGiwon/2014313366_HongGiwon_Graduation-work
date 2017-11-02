# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
from konlpy.tag import Twitter
import pickle
import os
import gensim
import multiprocessing

p = re.compile("[\u0000-\u001f\u0020\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff]")

def string_re(inputstring):
	m = p.findall(inputstring)
	return ("".join(m))

def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

class iter_txt2sen(object):

	def __init__(self, total_mum):
		self.file_count = total_mum

	def __iter__(self):

		for i in range(1,self.file_count+1) :
			txt_file = open(os.getcwd() + "/temp/crawlingResult" + str(i) + ".txt" ,'rb')
			for sentence in pickle.load(txt_file) :
				yield sentence


words = open("unlearned_word.txt","r").read().splitlines()
count = 0
sen_count = 0
word_count = 0

for word in words :
	corpus = []
	try :
		param = urllib.parse.quote(word).replace("%", ".")
		urlfront = 'http://search.dcinside.com'
		url = 'http://search.dcinside.com/post/q/' + param
		urlback = "/q/" + param

		data = urllib.request.urlopen(url).read()

		soup = BeautifulSoup(data, "lxml")

		link = soup.find_all("div", {"class": "thumb_txt"})

		link2 = soup.find('div', {"id": "dgn_btn_paging"}).findAll('a', href=True)

		lastPage = int(link2[-1]["href"][8:10].replace("/", ""))

		print("word: " + word)
		print("pages: 1 ~ " + str(lastPage))

		count = count + 1

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

				#get contents
				context = m2.p.getText()
				idx = context.rfind(" - ")
				context = context.replace(" - dc official App", "")
				#print(context.strip())
				sentence_token = flat(string_re(title) + " " + string_re(context).strip())
				corpus.append(sentence_token)
				sen_count = sen_count + 1
				word_count = word_count + len(sentence_token)
		
		crawlingResult = open(os.getcwd() + "/temp/crawlingResult" + str(count) + ".txt", "wb+")
		pickle.dump(corpus,crawlingResult)
		crawlingResult.close()

	except AttributeError:
		print ("크롤링이 불가능한 단어입니다 : " + word)

words.close()

clear_list = open("unlearned_word.txt","w")
clear_list.close()


unlearned_corpus = iter_txt2sen(count)
model = gensim.models.Word2Vec.load('model')
model.alpha = sen_count / model.total_sen_count
model.total_sen_count = model.total_sen_count + sen_count
model.build_vocab(unlearned_corpus, update=True)
#model.train(unlearned_corpus, total_examples=model.corpus_count, epochs=model.iter)
model.train(unlearned_corpus, total_examples=sen_count, total_words = word_count, epochs=model.iter)

model.save('model')
