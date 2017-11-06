import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Twitter
import os
import re
import random
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

p = re.compile("[\u0000-\u001f\u0020\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff]")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project-f557b58c64ab.json'

def sen_analysis_value(input_text):
    client = language.LanguageServiceClient()
    document = types.Document(
        content=input_text,
        type=enums.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(document).document_sentiment
    #print ("감정 분석 점수 : " + str(sentiment.score))
    return sentiment.score * 0.07

def string_re(inputstring):
    m = p.findall(inputstring)
    return ("".join(m))

def flat(content):
    token_tmp = Twitter().pos(content)
    return ["{}/{}".format(word, tag) for word, tag in token_tmp if (tag != "Punctuation"and tag != "Foreign")]

model = gensim.models.Word2Vec.load('model')
bad_word_vec = model.bad_word_vec
model_words_vec = model.wv
del model

model2 = gensim.models.Word2Vec.load('model2')
bad_word_vec2 = model2.bad_word_vec
model_words_vec2 = model2.wv
del model2
'''
parameterSim = [0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.70]
parameterSent = [0.01, 0.04, 0.07, 0.1, 0.14, 0.17, 0.2, 0.24, 0.27, 0.3]

scoreList = [[],[],[],[],[],[],[],[],[],[],[]]

for i in range(len(parameterSim)) :
    for j in range(len(parameterSent)) :
        scoreList[i].append([[],[],[],[]])

scorePointBadF = [[],[],[],[],[],[],[],[],[],[],[]]

for i in range(len(parameterSim)) :
    for j in range(len(parameterSent)) :
        scorePointBadF[i].append([0,0,0,0])

scorePointBadN = [[],[],[],[],[],[],[],[],[],[],[]]

for i in range(len(parameterSim)) :
    for j in range(len(parameterSent)) :
        scorePointBadN[i].append([0,0,0,0])

scorePointNormalF = [[],[],[],[],[],[],[],[],[],[],[]]

for i in range(len(parameterSim)) :
    for j in range(len(parameterSent)) :
        scorePointNormalF[i].append([0,0,0,0])

scorePointNormalN = [[],[],[],[],[],[],[],[],[],[],[]]

for i in range(len(parameterSim)) :
    for j in range(len(parameterSent)) :
        scorePointNormalN[i].append([0,0,0,0])
'''
#### index가 0이면 normal, 1이면 감정 분석, 2이면 추가학습된 모델, 3이면 감정분석 + 추가학습된 모델
scoreBadF = [0 for i in range (4)] #욕설인데 필터링함
scoreBadN = [0 for i in range (4)] #욕설인데 필터링하지 않음
scoreNormalF = [0 for i in range (4)] #욕설이 아닌데 필터링함
scoreNormalN = [0 for i in range (4)] #욕설이 아닌데 필터링하지 않음

testSet = open("testset.txt", "r", encoding='UTF8').read().splitlines()
senCount = 0
'''
for sentence in testSet :
    senCount = senCount + 1
    oriSentence = string_re(sentence)
    #print ("문장 : " + oriSentence)
    senScore = sen_analysis_value(oriSentence)

    sentenceList = sentence.split(" ")

    for psiIndex in range(len(parameterSim)) :
        for pseIndex in range(len(parameterSent)) :
            for i in range(0, len(sentenceList)) :
                tokenizied_word = flat(sentenceList[i].split(":")[0])
                scoreList[psiIndex][pseIndex][0].insert(i,"F")
                scoreList[psiIndex][pseIndex][1].insert(i,"F")
                scoreList[psiIndex][pseIndex][2].insert(i,"F")
                scoreList[psiIndex][pseIndex][3].insert(i,"F")
                for token_of_word in tokenizied_word :
                    try :
                        #if (model_words_vec2.vocab[token_of_word].count < 1000) : 
                            #print (" 학습이 부족한 단어 발견 : " + token_of_word)
                        if (cosine_similarity([bad_word_vec], [model_words_vec[token_of_word]])[0][0] > parameterSim[psiIndex]) :
                            #evalList[i] = "T"
                            scoreList[psiIndex][pseIndex][0][i] = "T"
                        if (cosine_similarity([bad_word_vec], [model_words_vec[token_of_word]])[0][0] > (parameterSim[psiIndex] + senScore * parameterSent[pseIndex])) :
                            #evalListSentiment[i] = "T"
                            scoreList[psiIndex][pseIndex][1][i] = "T"
                        if (cosine_similarity([bad_word_vec2], [model_words_vec2[token_of_word]])[0][0] > parameterSim[psiIndex]) :
                            #evalListSecondModel[i] = "T"
                            scoreList[psiIndex][pseIndex][2][i] = "T"
                        if (cosine_similarity([bad_word_vec2], [model_words_vec2[token_of_word]])[0][0] > (parameterSim[psiIndex] + senScore * parameterSent[pseIndex])) :
                            #evalListSecondModelSentiment[i] = "T"
                            scoreList[psiIndex][pseIndex][3][i] = "T"
                    except KeyError: 
                        #print("학습 안된 단어 : " + token_of_word + str(i))
                        pass



            for i in range(0, len(sentenceList)) :
                for number in range (0,4) :
                    if (sentenceList[i].split(":")[1] == "F" and scoreList[psiIndex][pseIndex][number][i] == "F") :
                        scorePointNormalN[psiIndex][pseIndex][number] = scorePointNormalN[psiIndex][pseIndex][number] + 1
                    elif (sentenceList[i].split(":")[1] == "T" and scoreList[psiIndex][pseIndex][number][i] == "T") :
                        scorePointBadF[psiIndex][pseIndex][number] = scorePointBadF[psiIndex][pseIndex][number] + 1
                    elif (sentenceList[i].split(":")[1] == "T" and scoreList[psiIndex][pseIndex][number][i] == "F") :
                        scorePointBadN[psiIndex][pseIndex][number] = scorePointBadN[psiIndex][pseIndex][number] + 1
                        #print("욕설인데 필터링 안함 문장 : " + str(senCount) + "단어 : " + sentenceList[i] + " 모델 : " + str(number))
                    elif (sentenceList[i].split(":")[1] == "F" and scoreList[psiIndex][pseIndex][number][i] == "T") :
                        scorePointNormalF[psiIndex][pseIndex][number] = scorePointNormalF[psiIndex][pseIndex][number] + 1
                        #print("욕설아닌데 필터링함 문장 : " + str(senCount) + "단어 : " + sentenceList[i] + " 모델 : " + str(number))

for psiIndex in range(len(parameterSim)) :
    for pseIndex in range(len(parameterSent)) :
        for number in range(0,4) :
            print ("\n------------------------------------------------------------------------------------------")
            print ("sim : " + str(parameterSim[psiIndex]))
            print ("sen : " + str(parameterSent[pseIndex]))
            if (number == 0) : print ("normal 모델\n")
            if (number == 1) : print ("normal 모델 + 감정 분석\n")
            if (number == 2) : print ("추가 학습된 모델\n")
            if (number == 3) : print ("추가 학습된 모델 + 감정 분석\n")
            #print ("욕설인데 필터링함 : " + str(scoreBadF[number]))
            #print ("욕설인데 필터링하지 않음 : " + str(scoreBadN[number]) + "\n")
            #print ("욕설이 아닌데 필터링함 : " + str(scoreNormalF[number]))
            #print ("욕설이 아닌데 필터링하지 않음 : " + str(scoreNormalN[number]) + "\n")
            print ("욕설을 필터링할 확률 : " + str(scorePointBadF[psiIndex][pseIndex][number] / (scorePointBadF[psiIndex][pseIndex][number] + scorePointBadN[psiIndex][pseIndex][number])))
            print ("잘못 필터링할 확률 : " + str(scorePointNormalF[psiIndex][pseIndex][number] / (scorePointNormalF[psiIndex][pseIndex][number] + scorePointNormalN[psiIndex][pseIndex][number])) + "\n")
'''

for sentence in testSet :
    senCount = senCount + 1
    oriSentence = string_re(sentence)
    #print ("문장 : " + oriSentence)
    senScore = sen_analysis_value(oriSentence)

    evalList = [[],[],[],[]]
    sentenceList = sentence.split(" ")

    for i in range(0, len(sentenceList)) :
        tokenizied_word = flat(sentenceList[i].split(":")[0])
        evalList[0].insert(i,"F")
        evalList[1].insert(i,"F")
        evalList[2].insert(i,"F")
        evalList[3].insert(i,"F")
        for token_of_word in tokenizied_word :
            try :
                if (model_words_vec2.vocab[token_of_word].count < 1000) : 
                    print (" 학습이 부족한 단어 발견 : " + token_of_word)
                if (cosine_similarity([bad_word_vec], [model_words_vec[token_of_word]])[0][0] > 0.6) :
                    evalList[0][i] = "T"
                if (cosine_similarity([bad_word_vec], [model_words_vec[token_of_word]])[0][0] > (0.6 + senScore)) :
                    evalList[1][i] = "T"
                if (cosine_similarity([bad_word_vec2], [model_words_vec2[token_of_word]])[0][0] > 0.6) :
                    evalList[2][i] = "T"
                if (cosine_similarity([bad_word_vec2], [model_words_vec2[token_of_word]])[0][0] > (0.6 + senScore)) :
                    evalList[3][i] = "T"
            except KeyError: 
                print("학습 안된 단어 : " + token_of_word + str(i))

    for i in range(0, len(sentenceList)) :
        for number in range (0,4) :
            if (sentenceList[i].split(":")[1] == "F" and evalList[number][i] == "F") :
                scoreNormalN[number] = scoreNormalN[number] + 1
            elif (sentenceList[i].split(":")[1] == "T" and evalList[number][i] == "T") :
                scoreBadF[number] = scoreBadF[number] + 1
            elif (sentenceList[i].split(":")[1] == "T" and evalList[number][i] == "F") :
                scoreBadN[number] = scoreBadN[number] + 1
                print("욕설인데 필터링 안함 문장 : " + str(senCount) + "단어 : " + sentenceList[i] + " 모델 : " + str(number))
            elif (sentenceList[i].split(":")[1] == "F" and evalList[number][i] == "T") :
                scoreNormalF[number] = scoreNormalF[number] + 1
                print("욕설아닌데 필터링함 문장 : " + str(senCount) + "단어 : " + sentenceList[i] + " 모델 : " + str(number))

for number in range(0,4) :
    print ("\n------------------------------------------------------------------------------------------")
    if (number == 0) : print ("normal 모델\n")
    if (number == 1) : print ("normal 모델 + 감정 분석\n")
    if (number == 2) : print ("추가 학습된 모델\n")
    if (number == 3) : print ("추가 학습된 모델 + 감정 분석\n")
    print ("욕설인데 필터링함 : " + str(scoreBadF[number]))
    print ("욕설인데 필터링하지 않음 : " + str(scoreBadN[number]) + "\n")
    print ("욕설이 아닌데 필터링함 : " + str(scoreNormalF[number]))
    print ("욕설이 아닌데 필터링하지 않음 : " + str(scoreNormalN[number]) + "\n")
    print ("욕설을 필터링할 확률 : " + str(scoreBadF[number] / (scoreBadF[number] + scoreBadN[number])))
    print ("잘못 필터링할 확률 : " + str(scoreNormalF[number] / (scoreNormalF[number] + scoreNormalN[number])) + "\n")
