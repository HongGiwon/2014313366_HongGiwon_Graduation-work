import pickle
from konlpy.tag import Kkma, Twitter

tokenized_output = open("tnamu_001.txt", 'rb')

tmplist = pickle.load(tokenized_output)
print(tmplist)

tmplist = pickle.load(tokenized_output)
print(tmplist)

tokenized_output.close()