# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import re
from konlpy.tag import Twitter
import pickle
import os
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import multiprocessing
from sklearn.metrics.pairwise import cosine_similarity
import random
import sys

p = re.compile("[\u0000-\u001f\u0020\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff]")

def string_re(inputstring):
	m = p.findall(inputstring)
	return ("".join(m))

def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

class iter_txt2sen(object):

	def __init__(self, total_mum, sen_num, mod_flag):
		self.file_count = total_mum
		self.each_sen_count = int(sen_num / 20)
		self.flag = mod_flag

	def __iter__(self):

		for i in range(1,self.file_count+1) :
			txt_file = open(os.getcwd() + "/temp/crawlingResult" + str(i) + ".txt" ,'rb')
			print(os.getcwd() + "/temp/crawlingResult" + str(i) + ".txt")
			for sentence in pickle.load(txt_file) :
				yield sentence

		#기존 dataset에서 sampling
		if (self.flag == True) :
			for i in range(1, 21) :
				ori_txt_file = open(os.getcwd() + "/dataset/toknamu_" + str(i) + ".txt" ,'rb')
				print(os.getcwd() + "/dataset/toknamu_" + str(i) + ".txt")
				for ori_sentence in random.sample(pickle.load(ori_txt_file),self.each_sen_count) :
					yield ori_sentence



def main(flag):
	words = open("unlearned_word.txt","r").read().splitlines()
	count = 0
	senCount = 0
	wordCount = 0
	random.seed()
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
					senCount = senCount + 1
					wordCount = wordCount + len(sentence_token)
			
			crawlingResult = open(os.getcwd() + "/temp/crawlingResult" + str(count) + ".txt", "wb+")
			pickle.dump(corpus,crawlingResult)
			crawlingResult.close()

		except IndexError:
			print ("크롤링이 불가능한 단어입니다 : " + word)
		except AttributeError:
			print ("크롤링이 불가능한 단어입니다 : " + word)

	clear_list = open("unlearned_word.txt","w")
	clear_list.close()

	unlearned_corpus = iter_txt2sen(count, senCount, flag)
	model = gensim.models.Word2Vec.load('model')
	model.alpha = 0.001 * senCount / model.total_sen_count
	model.total_sen_count = model.total_sen_count + senCount

	bad_words_sim_list = []
	for word, vocab_obj in model.wv.vocab.items():
		if (cosine_similarity([model.bad_word_vec],[model[word]])[0][0] > 0.6) : 
			if (word.split("/")[1] == "Noun") : bad_words_sim_list.append(word.split("/")[0])

	model.bad_words_sim_list = bad_words_sim_list


	model.build_vocab(unlearned_corpus, update=True)
	#model.train(unlearned_corpus, total_examples=model.corpus_count, epochs=model.iter)
	model.train(unlearned_corpus, total_examples=senCount, total_words = wordCount, epochs=model.iter)

	model.save('model2')

def exe_mod() :

	exeModFlag = False
	try :
		if (len(sys.argv) > 2) : 
			print ("입력된 파라미터 개수가 너무 많습니다.")
			exeModFlag = False

		if (sys.argv[1] == "--sample") : 
			exeModFlag = True

		else : 
			print ("정의되지 않은 입력입니다.")
			exeModFlag = False

	except IndexError :
		exeModFlag = False

	finally :
		if (exeModFlag == False) : print ("\n실행 : 기존 dataset에서 sampling을 수행하지 않습니다.")
		elif (exeModFlag == True) : print ("\n실행 : 기존 dataset에서 sampling을 수행합니다.")
		return exeModFlag

if __name__ == '__main__':
	modFlag = exe_mod()
	main(modFlag)