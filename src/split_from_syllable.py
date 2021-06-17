# -*- coding: utf-8 -*-

from jamo import h2j, j2hcj
from jamo_custom import split_syllable_char
import numpy as np
from difflib import SequenceMatcher
from functools import reduce
from itertools import chain

# def jamo_test(*args):
#     # print('args:', args)
#     jamo = []
#
#     for i in args:
#         jamo.append(j2hcj(h2j(i)))
#     x = []
#     x2 = []
#
#     for i in range(len(jamo)):
#         y = []
#
#         total = 0
#         for j in range(len(jamo[i])):
#             total += int(ord(jamo[i][j]) % 12593)
#             y.append(ord(jamo[i][j]) % 12593)  # ㄱ ~ ㅎ, ㅏ ~ ㅣ 까지의 유니코드가 12593 ~ 12643이므로 가장 작은 수인 12593으로 모듈러 연산을 수행 후 처리
#
#
#         x.append(y)
#         x2.append(total)
#             # print(ord(jamo[i][j]))
#         # print(type(jamo[i]))
#     print(jamo)
#     print(x)
#     # print(y)
#     # print('x2:', x2)
#
#     return x2
#
# test_university = ['가야', '가천', '가톨릭관동', '가톨릭', '가톨릭상지', '감리교신학', '강남', '강동', '강릉영동', '강릉원주', '강원관광', '강원', '강원도립', '거제', '건국', '건양', '건양사이버', '경기과학기술', '경기', '경남과학기술', '경남', '경남도립거창', '경남도립남해', '경남정보', '경동', '경민', '경복', '경북과학', '경북', '경북도립', '경북보건', '경북전문', '경상', '경성', '경운', '경인교육', '경인여자', '경일', '경주', '경희', '경희사이버', '계명', '계명문화', '계원예술', '고구려', '고려', '고려사이버', '고신', '공주교육', '공주', '광신', '광양보건', '광운', '광주가톨릭', '광주과학기', '광주교육', '광주', '광주보건', '광주여자', '구미', '국민', '국제', '국제사이버', '국제예술', '군산간호', '군산', '군장', '극동', '글로벌사이버', '금강', '금오공과', '기독간호', '김천', '김포', '김해', '꽃동네', '나사렛', '남부', '남서울', '농협', '단국', '대경', '대구가톨릭', '대구경북과학기', '대구공업', '대구과학', '대구교육', '대구', '대구보건', '대구사이버', '대구예술', '대구한의', '대덕', '대동', '대림', '대신', '대우조선해양공과', '대원', '대전가톨릭', '대전과학기술', '대전', '대전보건', '대전신학', '대진', '덕성여자', '동강', '동국', '동남보건', '동덕여자', '동명', '동부산', '동서', '동서울', '동신', '동아', '동아방송예술', '동아보건', '동양', '동양미래', '동우', '동원과학기술', '동원', '동의과학', '동의', '동주', '두원공과', '디지털서울문화예술', '루터', '마산', '명지', '명지전문', '목원', '목포가톨릭', '목포과학', '목포', '목포해양', '문경', '배재', '배화여자', '백석', '백석문화', '백석예술', '백제예술', '부경', '부산가톨릭', '부산경상', '부산과학기술', '부산교육', '부산', '부산디지털', '부산여자', '부산예술', '부산외국어', '부산장신', '부천', '사이버한국외국어', '삼성전자공과', '삼성중공업공과', '삼육', '삼육보건', '상명', '상지', '상지영서', '서강', '서경', '서라벌', '서영', '서울과학기술', '서울교육', '서울기독', '서울', '서울디지털', '서울사이버', '서울시립', '서울신학', '서울여자간호', '서울여자', '서울예술', '서울장신', '서울한영', '서원', '서일', '서정', '서해', '선린', '선문', '성결', '성공회', '성균관', '성신여자', '성심외국어', '성운', '세경', '세계사이버', '세명', '세종', '세종사이버', '세한', '송곡', '송원', '송원', '송호', '수성', '수원가톨릭', '수원과학', '수원', '수원여자', '숙명여자', '순복음총회신', '순천', '순천제일', '순천향', '숭실', '숭실사이버', '숭의여자', '신경', '신구', '신라', '신성', '신안산', '신한', '신흥', '아세아연합신학', '아주', '아주자동차', '안동과학', '안동', '안산', '안양', '여주', '연성', '연세', '연암공과', '연암', '영남', '영남사이버', '영남신학', '영남외국어', '영남이공', '영산', '영산선학', '영진사이버', '영진전문', '예수', '예원예술', '오산', '용인', '용인송담', '우석', '우송', '우송정보', '울산과학기', '울산과학', '울산', '웅지세무', '원광', '원광디지털', '원광보건', '위덕', '유원', '유한', '을지', '이화여자', '인덕', '인제', '인천가톨릭', '인천', '인천재능', '인하공업전문', '인하', '장로회신학', '장안', '전남과학', '전남', '전남도립', '전북과학', '전북', '전주교육', '전주기전', '전주', '전주비전', '정석', '정화예술', '제주관광', '제주국제', '제주', '제주한라', '조선간호', '조선', '조선이공', '중부', '중앙', '중앙승가', '중원', '진주교육', '진주보건', '진주산업', '차의과학', '창신', '창원', '창원문성', '청강문화산업', '청암', '청운', '청주교육', '청주', '초당', '총신', '추계예술', '춘천교육', '춘해보건', '충남', '충남도립', '충북', '충북도립', '충북보건과학', '충청', '침례신학', '칼빈', '케이씨', '평택', '포스코기술', '포항공과', '포항', '한경', '한국골프', '한국과학기', '한국관광', '한국교원', '한국교통', '한국국제', '한국기술교육', '한국농수산', '한국방송통신', '한국복지', '한국복지사이버', '한국산업기술', '한국성서', '한국승강기', '한국열린사이버', '한국영상', '한국예술종합', '한국외국어', '한국전통문화', '한국체육', '한국폴리텍', '한국항공', '한국해양', '한남', '한동', '한라', '한려', '한림', '한림성심', '한밭', '한북', '한서', '한성', '한세', '한신', '한양', '한양사이버', '한양여자', '한영', '한일장신', '현대중공업공과', '협성', '혜전', '호남', '호남신학', '호산', '호서', '호원', '홍익', '화신사이버']
# test_target = ['중양']
#
# compare_list = []
# for origin in test_university:
#     for target in test_target:
#         ratio = SequenceMatcher(None, target, origin).ratio()
#         if ratio >= 0.5:
#             compare_list.append(origin)
# jamo1 = jamo_test(*compare_list)
# jamo2 = jamo_test(*test_target)

def get_split_from_syllable(*args):
    r = []
    for i in range(len(args)):
        a = []
        for j in range(len(args[i])):
            a.append(split_syllable_char(args[i][j]))
        r.append(a)
    # print(r)
    return r

def get_unicode(*args):
    HANGUL_INDEX = 12593

    result = []
    for i in range(len(args)):
        for j in range(len(args[i])):
            r = []
            for k in range(len(args[i][j])):
                tmp = []
                for l in range(len(args[i][j][k])):
                    if args[i][j][k][l] is not None:
                        tmp.append(ord(args[i][j][k][l]) % HANGUL_INDEX)
                    else:
                        tmp.append(-1) # -1 == 'None'
                r.append(tmp)
            result.append(r)
    # print(f'list = {result}')
    return result
# def get_unicode_from_split(*args):
#     print(f'args: ', list(chain.from_iterable(args)))
#     # print('ar:', z)
#     # args = list(chain.from_iterable(args))
#     result = []
#     HANGUL_INDEX = 12593
#     for i in range(len(args)):
#         for j in range(len(args[i])):
#             print(args[i][j])
#             for k in range(len(args[i][j])):
#                 tmp = []
#                 for l in range(len(args[i][j][k])):
#                     if args[i][j][k][l] is not None:
#                         tmp.append(ord(args[i][j][k][l]) % HANGUL_INDEX)
#                         print(ord(args[i][j][k][l]) % HANGUL_INDEX, end=' ')
#                 result.append(tmp)
#                 print('')
#
#
#     print(result)
#     # print(r[2], len(r[2]))
#
# print(compare_list)
# print(jamo1)
# print(test_target)
# print(jamo2)