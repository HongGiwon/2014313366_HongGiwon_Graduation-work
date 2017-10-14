def flat(content):
    return ["{}/{}".format(word, tag) for word, tag in Twitter().pos(content)]

import codecs
import pickle
from konlpy.tag import Twitter

input_dump = codecs.open("pnamu_001.txt", 'r', "utf-8")
tokenized_output = open("tmp.txt", 'wb')

count = 0

while (True) :
	
	if (count % 1000 == 0) : print (count)
	if (count == 100) : break
	count = count + 1

	dump_line = input_dump.readline()
	if not dump_line : break

	if (dump_line == "\n") : 
		continue

	tmp = flat(dump_line)
	if (len(tmp) == 0) :
		continue
	
	#바이너리 형식으로 토크나이징 된 결과물을 저장함.
	pickle.dump(tmp,tokenized_output)

input_dump.close()
tokenized_output.close()