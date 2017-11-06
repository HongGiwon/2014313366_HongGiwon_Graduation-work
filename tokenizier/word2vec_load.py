# 토크나이징 된 단어들을 이용하여 word2vec을 학습시키는 코드

import pickle
import gensim
from sklearn.metrics.pairwise import cosine_similarity

model = gensim.models.Word2Vec.load('model')

#print(model.most_similar(positive=["서울/Noun", "일본/Noun"], negative=["한국/Noun"], topn=5))
#model.wv.most_similar_cosmul

#print(model["사람/Noun"][0])

bad_base_vec = []

#대표 욕설 단어
bad_base = ["뒈지/Verb","씹새끼야/Noun","개객기/Noun","샛기/Noun","멍청이/Noun","씹/Verb","똘추새끼/Noun","개색끼/Noun","씨부럴/Noun","염병할/Exclamation","시발/Noun","개새/Noun","잡년/Noun","ㅅㅂㄴ/KoreanParticle","씹할롬/Noun","개자식/Noun","지랄/Noun","쌔끼/Noun","럴/Noun","벌놈/Noun","저능/Noun","시팔/Noun","쉐끼들/Noun","놈/Noun","간나/Noun","럴놈/Noun","염병/Noun","옘병/Noun","색휘/Noun","창놈/Noun","썅놈/Noun","씨팔/Noun","좆/Noun","썅/Noun","창년/Noun","쌍놈/Noun","니미/Noun","앰창/Noun","엠창/Noun","썅년/Noun","똘추/Noun","느금마/Noun","븅딱/Noun","개돼지/Noun","개썅놈/Noun","개새끼/Noun","씨발/Noun","존나/Noun","시벌/Noun","애미/Noun"]

for word in bad_base :
	bad_base_vec.append(model[word])

#대표 욕설 단어들의 벡터 값 합의 평균 벡터
bad_word_vec = [sum(x)/len(bad_base_vec) for x in zip(*bad_base_vec)]
bad_word_vec = [ x - y/5 for x,y in zip(bad_word_vec,model["ㅋㅋㅋ/KoreanParticle"])]
bad_word_vec = [ x + y/10 for x,y in zip(bad_word_vec,model["애미/Noun"])]

print(cosine_similarity([bad_word_vec], [model["씨발/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["서울/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["개새끼/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["앰창/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["음료수/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["애비/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["애미/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["병신/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["ㅋㅋㅋ/KoreanParticle"]]))
print(cosine_similarity([bad_word_vec], [model["개웃/Adverb"]]))
print(cosine_similarity([bad_word_vec], [model["니애미/Noun"]]))
print(cosine_similarity([bad_word_vec], [model["그니까/Conjunction"]]))
print(cosine_similarity([bad_word_vec], [model["시발/Noun"]]))




print(model.similarity('ㅋㅋㅋ/KoreanParticle', '개웃/Adverb'))
print(model.alpha)

wvector = model.wv
del model

print(wvector.vocab["니애미/Noun"].count)
print("븅신/Noun".split("/")[0])

print(cosine_similarity([bad_word_vec], [wvector["븅신/Noun"]]))
print(cosine_similarity([bad_word_vec], [wvector["씨발/Noun"]]))
print(cosine_similarity([bad_word_vec], [wvector["서울/Noun"]]))
print(cosine_similarity([bad_word_vec], [wvector["개새끼/Noun"]]))
print(cosine_similarity([bad_word_vec], [wvector["앰창/Noun"]]))
print(cosine_similarity([bad_word_vec], [wvector["음료수/Noun"]]))



try :
	print(model["ㅁㅇㅁㅇ"])

except KeyError:
	print ("학습이 안됬네")

