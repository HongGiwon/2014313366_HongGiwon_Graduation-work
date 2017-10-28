# 토크나이징 된 단어들을 이용하여 word2vec을 학습시키는 코드

import pickle
import gensim

model = gensim.models.Word2Vec.load('model')

print(model.most_similar(positive=["서울/Noun", "일본/Noun"], negative=["한국/Noun"], topn=5))
#model.wv.most_similar_cosmul

print(model.most_similar(positive=["지구/Noun"], negative=["생명/Noun"], topn=5))

print(model.most_similar(positive=["사람/Noun"], negative=["지능/Noun"], topn=5))

print(model.most_similar(positive=["개새끼/Noun", "씨발/Noun"], topn=5))

#print(model.most_similar_cosmul(positive=["개새끼/Noun"], topn=10))