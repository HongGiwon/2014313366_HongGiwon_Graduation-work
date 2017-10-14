import codecs
import pickle
from konlpy.tag import Kkma, Twitter

input_dump = codecs.open("pnamu_001.txt", 'r', "utf-8")
tokenized_output = open("tnamu_001.txt", 'wb')

con = input("입력 : ")
while (con == 'y') :

	dump_line = input_dump.readline()
	if (dump_line == "\n") : 
		continue

	tmp = Twitter().pos(dump_line)
	if (len(tmp) == 0) :
		continue
	
	pickle.dump(tmp,tokenized_output)

	con = input("입력 : ")

input_dump.close()
tokenized_output.close()