# 2014313366_HongGiwon_Graduation-work

학습 데이터는 나무위키의 데이터 베이스를 NamuMarkAST(https://github.com/MerHS/biryo)
를 이용하여 추출해 html 태그, 특수 문자 등을 제거하여 정제함

데이터 전처리 과정

1. parser로 dump json -> txt
2. editplus로 html 태그 제거
3. editplus로 리다이렉트 상위 문서 제거
4. refine.java로 특수문자 제거(정규화 기반)
5. editplus [0-99][.] 제거
6. 문장단위 구분
7. 토크나이징
8. 토크나이징 시 영어, 느낌표, 숫자, 특수문자 제거해서 저장하
