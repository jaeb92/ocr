# from utils import get_jamo_uni, jamo_to_unicode
# import numpy as np
# import itertools
from difflib import SequenceMatcher
# tmp = ['미디어디자인컨렌손학부']
# education = ['미디어디자인컨렌츠학과', '미디어디자인컨텐츠학부', '미디어디자인학부', '디지털미디어비즈니스학과', '디지털미디어전공']
#
# univ_list = []
# max = 0
# max_edu = ''
# for edu in education:
#     for t in tmp:
#         edu_sum, edu_split = get_jamo_uni(edu)
#         t_sum, t_split = get_jamo_uni(t)
#
#         edu_split = list(itertools.chain.from_iterable(edu_split))
#         t_split = list(itertools.chain.from_iterable(t_split))
#
#         if len(edu_split) == len(t_split):
#             print(f"{edu}: {edu_split}\n{t}: {t_split}\n")
#
#             t1 = np.array(jamo_to_unicode(*edu_split))
#             t2 = np.array(jamo_to_unicode(*t_split))
#             # print(f"{edu} : {t1}\n{t}: {t2}\n")
#             # print(t1 == t2)
#             same_count = sum(t1 == t2)
#             print(same_count)
#             # print('same count: ', t1==t2)
#
#             if max < same_count:
#                 max = same_count
#                 max_edu = edu
#
# univ_list.append(max_edu)
# print(univ_list)

import psycopg2
import sqlalchemy
import pandas as pd
# from db import dbconn
# db = dbconn.Database('aki05', 'dkzlxprxm123', 'ocr_db')
# sql = 'select 학과명 from pdftest.major_list order by 학과명 asc'
# data = db.select(sql)
# print(data.shape)
# data = data.drop_duplicates()
#
# print(data.shape)
# print(data[data['학과명'] == '초등컴퓨터교육전공'])

university = '한성대학교'
a = '복수전공'
from db import dbconn
import os
print(os.getcwd())
import sys
print(sys.path)

sql = "select distinct 학과명 from pdftest.major_list where 학교명 = '" + university + "' order by 학과명 asc"
db = dbconn.Database('aki05', 'dkzlxprxm123', 'ocr_db')
b = db.select(sql)['학과명'].tolist()
print(b)
max = 0
for i in b:
    s = SequenceMatcher(None, a, i).ratio()
    if max < s:
        max_univ = i
        max = s

print(f"{max_univ} >> {max}")