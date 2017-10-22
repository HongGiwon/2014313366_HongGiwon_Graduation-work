# 토크나이징 된 단어들을 이용하여 word2vec을 학습시키는 코드

import pickle
import gensim

model = gensim.models.Word2Vec.load('model')

print(model.most_similar(positive=["서울/Noun"], negative=["일본/Noun"], topn=5))


