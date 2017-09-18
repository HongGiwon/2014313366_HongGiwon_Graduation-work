def main():

    testStr = input() # 문자열 입력
    wordList = testStr.split() # 문자열을 공백으로 구분하여 리스트에 단어저장

    dic={} # dictionary 선언
    flag = False # flag 선언
    
    db = open('./badwords.txt', 'r') # 욕설 데이터베이스 열기
    while True:
        word = db.readline() # 데이터베이스에서 줄단위로 욕설을 읽어드린다
        if word == '':break # 공백일 경우 중단
        word = word[:-1] # 줄바꿈(enter) 제거
        dic[word] = 1 # dictionary에 value를 1로 저장
    db.close()

    for i in wordList: # 단어가 저장된 리스트에서
        if i in dic: # 단어가 딕셔너리에 있다면(욕설이라면)
            flag = True # flag를 트루로 리턴
    
    print(flag)
    

main()
