def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

import codecs
import pickle
from konlpy.tag import Twitter
import re

corpus = []

count = 0

for i in range(7,8) :

	print (i)
	input_dump = codecs.open("pnamu_020.txt", 'r', "utf-8")
	tokenized_output = open("toknamu_00" + str(i) + ".txt", 'wb')

	while (True) :
	
		if (count % 100 == 0) : print (count)
		count = count + 1

		print (count)
		dump_line = input_dump.readline()

		if not dump_line : break

		print (count)
		if (len(dump_line) < 5) : 
			continue
		print (count)
		token_tmp = Twitter().pos(dump_line)
		print (count)
		tokenized_sentence = ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation" and tag != "Foreign")]

		if (len(tokenized_sentence) == 0) :
			continue

		print (count)
		corpus.append(tokenized_sentence)


	#바이너리 형식으로 토크나이징 된 결과물을 저장함.
	pickle.dump(corpus,tokenized_output)
	print (count)

	input_dump.close()
	tokenized_output.close()

