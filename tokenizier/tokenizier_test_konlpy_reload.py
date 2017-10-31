# 토크나이징 된 단어들을 이용하여 word2vec을 학습시키는 코드

import pickle
import gensim
import os
import multiprocessing

class iter_multxt2sen(object):

    def __init__(self, top_dir):
        self.file_list = []
        for root, dirs, files in os.walk(top_dir) :
        	for fname in filter(lambda fname: fname.endswith('.txt'), files) :
        		self.file_list.append(os.path.join(root, fname))

    def __iter__(self):

    	for filename in self.file_list :
    		print (filename)
    		txt_file = open(filename,'rb')
    		for sentence in pickle.load(txt_file) :
    			yield sentence

corpus = iter_multxt2sen(os.getcwd() + "/result")

#word2vec 모델의 설정
config = {
    'min_count': 10,
    'size': 300,
    'sg': 1,
    'batch_words': 10000,
    'iter': 15,
    'workers': multiprocessing.cpu_count() - 1
}

#모델 생성
model = gensim.models.Word2Vec(**config)

#모델 사전 생성 및 학습
print ("사전 생성")
model.build_vocab(corpus, update=False)
print ("학습 시작")
model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)

print ("저장 시작")
#모델 저장
model.save('model')

#모델 단어 개수 출력
print(len(model.wv.vocab))

#online 학습
#model.build_vocab(corpus, update=True)
#model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)

#두 단어의 유사성 예시
print(model.similarity('카메라/Noun', '유튜브/Noun'))