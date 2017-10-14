import codecs
from konlpy.tag import Kkma, Twitter

tmp = Twitter().pos("프로젝트에 참여해서 관련 문서에 기여의 손길을 보내주세요!")


input_dump = codecs.open("namu_001.txt", 'r', "utf-8")

dump_line = input_dump.readline()
print(dump_line)

input_dump.close()