# 토크나이징 된 단어들을 이용하여 word2vec을 학습시키는 코드

import pickle
import gensim

tokenized_output = open("toknamu_020.txt", 'rb')

#corpus = []

#토크나이징 된 단어들을 읽어서 corpus에 저장
#try : 
#	while (True) :
#
#		tmplist = pickle.load(tokenized_output)
#		corpus.append(tmplist)
#
#except EOFError :
#	print ("EOF")
#	tokenized_output.close()

corpus = pickle.load(tokenized_output)
tokenized_output.close()

#word2vec 모델의 설정
config = {
    'min_count': 1,
    'size': 300,
    'sg': 1,
    'batch_words': 10000,
    'iter': 10
}

#모델 생성
model = gensim.models.Word2Vec(**config)

#모델 사전 생성 및 학습
model.build_vocab(corpus)
model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)

#모델 저장
model.save('model')
#model = gensim.models.Word2Vec.load('model')

#두 단어의 유사성 예시
print(model.similarity('카메라/Noun', '유튜브/Noun'))