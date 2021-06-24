# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
#import pandas as pd
# from databases import dbconn
# db = dbconn.Database()
# data = db.select("select * from major_list")
# t = '미술학과'
# t = '과학기술대학'
# major = data['학과명']
# print(f'전공명 : {major}')
#
# if t in major.to_list():
#     print(f'{t} in major list')
# else:
#     print('nothing')
import re
from ocr_matcher import Matcher
from utils import alphabet_to_hangul

# univ_pattern = r"[가-힣a-zA-Z]{2,}대학교?"
# p_univ = re.compile(univ_pattern)
#
# contents = ['[원본확인번호', '1234567890]', '제', '1-010065호', '졸', '업', '증명서', '성', '명', '김호준', '생년월일', '1986년8월', '17일', '학', '과(부)', '영어영문학부', '전', '공', '영어학(영문학,', '영어학)', '졸업일', '자', '2009', '2.', '20', '학위등록번호', '한성대2008(학)0102', '복수전공', '무역학', '부전공', '*****', '연계전공', '*****', '전공학위명', '문학사,경영학사', '위의', '사실올', '증명함.', '202/년', '1월', '11일', '@히복','안성대학교', '한상대학교', '총', '학화', '[r', '*본증명서논해당대학및웬민원센터통페이지(wWw.webminwon.com)에서원본확인문서번호름통해원본대조가가능(발급', '후90일간)*제출용은칼라프린터', '출력올권장']
# with Matcher(['name', 'university', 'major', 'id', 'date']) as matcher:
#     text, major_list, univ_list, name_list, id_list, date_list = matcher.match(contents)
#
#     print(f"전공 후보: {major_list}")
#     print(f"대학교 후보: {univ_list}")
#     print(f"이름 후보: {name_list}")
#     print(f"아이디 후보: {id_list}")
#     print(f"날짜 후보: {date_list}")














# alphabet_to_hangul('I')
# alphabet_to_hangul('C')
# alphabet_to_hangul('T')


# 한성대학교:
# word = [('ㅎ', 'ㅏ', 'ㄴ'), ('ㅅ', 'ㅓ', 'ㅇ'), ('ㄷ', 'ㅐ', None), ('ㅎ', 'ㅏ', 'ㄱ'), ('ㄱ', 'ㅛ', None)]
# # # 한섬대학교:
# target = [('ㅎ', 'ㅏ', 'ㄴ'), ('ㅅ', 'ㅓ', 'ㅁ'), ('ㄷ', 'ㅐ', None), ('ㅎ', 'ㅏ', 'ㄱ'), ('ㄱ', 'ㅛ', None)]
# #
# #
# HANGUL_INDEX = 12593
#
# result = []
# for syl in word:
#     for i, jamo in enumerate(syl):
#         if jamo is not None:
#             jamo_uni = ord(jamo)
#         else:
#             jamo_uni = -1
#
#         result.append(jamo_uni % HANGUL_INDEX)
#         # print(jamo, jamo_uni, end=' ')
#
# print(result)
# for o, t in zip(origin, target):
#     for (_, z), (_, y) in zip(enumerate(o), enumerate(t)):
#         if z != None or y != None:
#             uni = ord(z)
#             print(z, ord(z), y, ord(y))
#         else:
#
#             print()
#         # print(a end=' ')
# 한중대학교: [('ㅎ', 'ㅏ', 'ㄴ'), ('ㅈ', 'ㅜ', 'ㅇ'), ('ㄷ', 'ㅐ', None), ('ㅎ', 'ㅏ', 'ㄱ'), ('ㄱ', 'ㅛ', None)]
# 한섬대학교: [('ㅎ', 'ㅏ', 'ㄴ'), ('ㅅ', 'ㅓ', 'ㅁ'), ('ㄷ', 'ㅐ', None), ('ㅎ', 'ㅏ', 'ㄱ'), ('ㄱ', 'ㅛ', None)]
import json
from utils import save_result
import pprint

id = '124124'
sample = {
    "university": [
      "한성대학교"
    ],
    "major": [
      "컴퓨터공학과",
      "연계전공"
    ],
    "name": [
      "홍길동"
    ],
    "date": [
      "2011년 12월 21일",
      "1991년5월 3일 2018.",
      "2018. 2. 20"
    ],
    "id": [
      "한성대2017(학)4001"
    ]
}

# save_result(r'../out/dict_result/result.json', sample, id)
with open(r'../out/dict_result/result.json', 'r+', encoding='utf-8-sig') as f:
    j = f.read()
    json_obj = json.loads(j)

print(json_obj['20210622_174428123'])
# # with open(r'./test.json', 'a+', encoding='utf-8') as f:
# #   json.dumps(sample)
# with open(r'../out/dict_result/result.json', 'r+', encoding='utf-8-sig') as f:
#   j = f.read()
#   # print(j)
#   json_obj = json.loads(j)
#   json_obj[id] = sample
#
# with open(r'../out/dict_result/result.json', 'w+', encoding='utf-8-sig') as f:
#     f.write(json.dumps(json_obj, ensure_ascii=False))
# # pprint.pprint(json_obj)
#   # f.write(json.dumps(j1))
#
