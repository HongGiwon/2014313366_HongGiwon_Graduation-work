def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation" and tag != "Alpha" and tag != "Foreign")]

def xplit(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)

import codecs
import pickle
from konlpy.tag import Twitter
import re


count = 0

for i in range(1,2) :

	print (i)
	input_dump = codecs.open("refinenamu_0021.txt", 'r', "utf-8")
	tokenized_output = open("toknamu_00" + str(i) + ".txt", 'wb')

	while (True) :
	
		if (count % 100 == 0) : print (count)
		count = count + 1
		dump_line = input_dump.readline()
		if not dump_line : break

		if (dump_line == "\n") : 
			continue
		try :

			for sentmp in xplit('.', '?', '!', '\n', '.\n')(dump_line) :
				
				if (len(sentmp) <= 2) :
					continue
				tmp = flat(sentmp)

				if (len(tmp) == 0) :
					continue

				#바이너리 형식으로 토크나이징 된 결과물을 저장함.
				pickle.dump(tmp,tokenized_output)
		except :
			continue
	print (count)
	count = 0
	input_dump.close()
	tokenized_output.close()

