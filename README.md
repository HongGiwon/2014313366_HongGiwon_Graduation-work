# 2014313366_HongGiwon_Graduation-work

학습 데이터는 나무위키의 데이터 베이스를 NamuMarkAST(https://github.com/MerHS/biryo)
를 이용하여 추출해 html 태그, 특수 문자 등을 제거하여 정제함

데이터 전처리 과정

1. parser로 dump json -> txt
2. editplus(텍스트 에디터)로 html 태그, 리다이렉트, 상위 문서 등의 위키 문법 텍스트 제거
4. refine.java로 특수문자 제거(정규화 기반)
5. 텍스트 에디터로 한글, control 문자, 숫자, 공백을 제외한 모든 문자 제거. ([^\u0000-\u001f\u0020\u0030-\u0039\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\uac00-\ud7af\ud7b0-\ud7ff])
5. 텍스트 에디터로 [0-99][.] 같은 일부 위키 문법 텍스트 추가 제거
6. 문장 부호 (. ? !)를 기반으로 문장 단위로 나눔
7. 토크나이징(konlpy-twitter)
