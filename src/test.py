# # -*- coding: utf-8 -*-
# # from utils import get_jamo_uni, jamo_to_unicode
# # import numpy as np
# # import itertools
# import os
# from difflib import SequenceMatcher
# # tmp = ['미디어디자인컨렌손학부']
# # education = ['미디어디자인컨렌츠학과', '미디어디자인컨텐츠학부', '미디어디자인학부', '디지털미디어비즈니스학과', '디지털미디어전공']
# #
# # univ_list = []
# # max = 0
# # max_edu = ''
# # for edu in education:
# #     for t in tmp:
# #         edu_sum, edu_split = get_jamo_uni(edu)
# #         t_sum, t_split = get_jamo_uni(t)
# #
# #         edu_split = list(itertools.chain.from_iterable(edu_split))
# #         t_split = list(itertools.chain.from_iterable(t_split))
# #
# #         if len(edu_split) == len(t_split):
# #             print(f"{edu}: {edu_split}\n{t}: {t_split}\n")
# #
# #             t1 = np.array(jamo_to_unicode(*edu_split))
# #             t2 = np.array(jamo_to_unicode(*t_split))
# #             # print(f"{edu} : {t1}\n{t}: {t2}\n")
# #             # print(t1 == t2)
# #             same_count = sum(t1 == t2)
# #             print(same_count)
# #             # print('same count: ', t1==t2)
# #
# #             if max < same_count:
# #                 max = same_count
# #                 max_edu = edu
# #
# # univ_list.append(max_edu)
# # print(univ_list)
#
# import psycopg2
# import sqlalchemy
# import pandas as pd
# # from db import dbconn
# # db = dbconn.Database('aki05', 'dkzlxprxm123', 'ocr_db')
# # sql = 'select 학과명 from pdftest.major_list order by 학과명 asc'
# # data = db.select(sql)
# # print(data.shape)
# # data = data.drop_duplicates()
# #
# # print(data.shape)
# # print(data[data['학과명'] == '초등컴퓨터교육전공'])
#
# import re
# import glob
#
# sw_path = r'D:\dv_21\opencv\stop_words\*.txt'
# sw_file_list = [file[:] for file in glob.glob(sw_path)]
#
# def character_cleaner(text):
#     # text = ' '.join(text)
#     text = re.sub('[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
#     return text
#
#
# # 공백제거 replace
# def space_cleaner(data):
#     data = [x.replace(' ', '') for x in data]
#     return data
#
#
# # 불용어 제거
# def stopword_cleaner(text: str) -> str:
#     stopwords = []
#     for filename in sw_file_list:
#         with open(filename, "r", encoding='UTF-8') as f:
#             stopwords += [line[:-1] for line in f.readlines()]
#         # print('stopwords', stopwords)
#         # f.close()
#     text = " " + text + " "
#     try:
#         text = re.sub("(?<![a-zA-Z가-힣0-9<>])(" + '|'.join(stopwords) + ")(?![a-zA-Z가-힣0-9<>])", " ", text)
#     except Exception as e:
#         print(e)
#
#     return text
#
# def clean_text_test():
#     # data = ['학위등록번호']
#     data = ['민원번호', '제Y1-11148', '호', '졸업증명서', '성', '명', '남보현', '생년', '월', '일', '1995년9월17일', '대학및학과(전공)', '예술체육대학체육학부(체육학전공)', '입학년월', '일', '2015년3월2일', '<', '졸업년월', '일', '2019년8월21', '일', '학위등록번호', '명지대18(학)2510', '학위명', '체육학사', '8', 'I', '지대학', '위의사실올증명합니다.', '2021년', '5월', '21일', '(메리혜팩', '명지대학교총@기증', '(i질표', '(자동발급기)', '*자동증명발급', '직인이없으면무료입니다.', '*본증명서는해당대학및웬민원센터흉페이지(WWWwebminwoncom)예서원본화인문서번호틀통해원본대조가가능합니다(발급후90일간)', '9']
#     cleaned_data = space_cleaner(data)
#     # print('cleaned_data:', cleaned_data)
#     text = ','.join(cleaned_data)
#     print('a:', text)
#     text = character_cleaner(text)
#     # print('ch clean: ', text)
#     text = stopword_cleaner(text)
#     return text
#
#
#
# f = clean_text_test()
# print('final:', f)
# def find_major_test():
#     university = '명지대학교'
#     cand = ['대학및학과', '예술체육대학체육학부']
#     from db import dbconn
#     import os
#     print(os.getcwd())
#     import sys
#     print(sys.path)
#
#     sql = "select distinct 학과명 from pdftest.major_list where 학교명 = '" + university + "' order by 학과명 asc"
#     db = dbconn.Database('aki05', 'dkzlxprxm123', 'ocr_db')
#     major_db = db.select(sql)['학과명'].tolist()
#     print('db 조회 결과: ', major_db)
#     major = 0
#     for m in major_db:
#         for c in cand:
#             s = SequenceMatcher(None, c, m).ratio()
#             if s > 0.5:
#                 print('유사도 0.5 이상 학과 >', m , s)
#                 if c == m or c in m or m in c:
#                     major = m
#
#     print('major:', major)
#     # print(f"{major}")
#
#     # t = a[0].split()
#
#     # a = list(map(lambda x: x.replace('년', '-').replace('월', '-').replace('일', '').replace('.', '-'), a))
#     # a = list(map(lambda x: x[0] for b in x, a))
#     # print(ord('0'), ord('9'))
#     # for i in a:
#     #     print(i)
#
# # find_major_test()

# t = ['a', 'b', 'c', 'd']
# print(t.index('a'))
#
# import MeCab
# m = MeCab.Tagger()
# a = m.parse('조직도')
# print(a)
# import re
#
#
# text = ['[원본확인번호', '1234567890]', '제', 'F-004225호', '졸', '업', '증명서', '성', '명', '최운경', '생년월일', '1986년6월', '6일', '학', '과(부)', '영어영문학부', '전', '공', '영어영문(영문학,', '영어학', '심화전공)', '졸업일', '자', '2012.', '8.', '17.', '학위등록번호', '한성대2017(학)1135', '복수전공', '*****', '부전공', '*****', '연계전공', '*****', '전공학위명', '문학사', '위의', '사실올', '증명함.', '202/년', '1월', '18일', '@히복', '한성대학교', '총', '학화', '[r', '*본증명서논', '자동발급기에서발급된것임', '*본증명서논해당대학및웬민원센터통페이지(wWw.webminwon.com)에서원본확인문서번호름통해원본대조가가능(발급', '후90일간)*제출용은칼라프린터', '출력올권장']
#
# date_pattern = r'^[\w가-힣]+((19[0-9][0-9]|20\d{2}|202/)[-년\s\\.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s\\.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1])[일\\.]?)?$'
# p = re.compile(date_pattern)
#
# l = list(map(lambda x: p.match(x), text))
#
# print(l)
import re
# sw = ['입학년도', '졸업증명합니다.', '졸업년도']
#
# s = ['1995년2월 졸업증명합니다. 23일2019.', '입학년도1992년 2월 12일', '12월', '31일', '입학년도', '2021년9월입학년도2021', '2021졸업년도2021년2월21일']
# n = []
# for w in sw:
#     for i, t in enumerate(s):
#         if w in t:
#             f = t.find(w)
#             if f > 0:
#                 t = t[:f] + ' ' + t[f+len(w):]
#             elif f == 0:
#                 t = t[f+len(w):]
#             else:
#                 pass
#             print(s[i], '>> ', t)
#         else:
#             print(t)
            # print(t[f:f+len(w)])

# print(t)
# print(text)
import re
p_d = re.compile(r'^((([가-힣]{1,})?\s?(19|20)\d{2}|202/)[\-년\s.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1]|[0-9])([일.\s])?)?$')
m = re.match(p_d, '1990년2월')
print(m)
# date_dict = {'birth_dt': '1990년2월 22일 2018', 'certification_dt': '2020.02.26', 'graduation_dt': '2014 03 03'}
# p1 = r'^[(19)|(20)]([0-9]{2})년'
# for index, (key, value) in enumerate(date_dict.items()):
#     if value == r'^[0-9]{4,}$'
# date_keys = date_dict.keys()
# t = list(map(lambda x: date_dict[x].replace('. ', '.'), date_keys))
# print(t)
# t = list(map(lambda x: x.replace('-', '.').replace('. ', '.').replace(' ', '.'), t))
# date_cdd = list(map(lambda x: x.replace('년', '').replace('월', '').replace('일', ''), t))
# date_dict = {key: date_cdd[i] for i, key in enumerate(date_keys)}
#
# print(date_dict)
