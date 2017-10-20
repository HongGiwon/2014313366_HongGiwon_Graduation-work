def flat(content):
	token_tmp = Twitter().pos(content)
	return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation" and tag != "Alpha" and tag != "Foreign")]

import codecs
import pickle
from konlpy.tag import Twitter

input_dump = codecs.open("refinenamu_001.txt", 'r', "utf-8")
tokenized_output = open("toknamu_001.txt", 'wb')

count = 0

while (True) :
	
	if (count % 1000 == 0) : print (count)
	if (count == 30) : break
	count = count + 1

	dump_line = input_dump.readline()
	if not dump_line : break

	if (dump_line == "\n") : 
		continue

	tmp = flat(dump_line)
	if (len(tmp) == 0) :
		continue
	print (tmp)
	print (tmp[0])
	
	#바이너리 형식으로 토크나이징 된 결과물을 저장함.
	pickle.dump(tmp,tokenized_output)

input_dump.close()
tokenized_output.close()