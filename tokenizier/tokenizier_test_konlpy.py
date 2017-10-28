def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

import codecs
import pickle
from konlpy.tag import Twitter
import re

for i in range(1,21) :

	corpus = []
	count = 0

	input_dump = codecs.open("pnamu_" + str(i) + ".txt", 'r', "utf-8")

	while (True) :
	
		if (count % 100 == 0) : print (count)
		
		count = count + 1
		dump_line = input_dump.readline()

		if not dump_line : break

		if (len(dump_line) < 5) : 
			continue

		token_tmp = Twitter().pos(dump_line)
		tokenized_sentence = ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation" and tag != "Foreign")]

		if (len(tokenized_sentence) == 0) :
			continue


		corpus.append(tokenized_sentence)

	input_dump.close()
	#바이너리 형식으로 토크나이징 된 결과물을 저장함.
	tokenized_output = open("toknamu_" + str(i) + ".txt", 'wb')
	pickle.dump(corpus,tokenized_output)
	tokenized_output.close()

