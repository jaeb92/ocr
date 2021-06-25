import os
import time
import glob
import MeCab
import re
import pandas as pd
import numpy as np
import itertools

from collections import OrderedDict
from log_config import set_logger
from hangul_romanize import Transliter
from hangul_romanize.rule import academic
from utils import get_split_from_syllable, get_jamo_uni, get_unicode, jamo_to_unicode
from difflib import SequenceMatcher
import dbconn

db = dbconn.Database("aki05", "dkzlxprxm123", "ocr_db")

logger = set_logger()
m = MeCab.Tagger()
syn_path = r'../synonym/syn_education.csv'
education_path = r'../res/csv/result.csv'
education = pd.read_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig')['education'].tolist()
syn_file_list = [file[:] for file in glob.glob(syn_path)]
transliter = Transliter(academic)

sw_path = r'D:/dv_21/opencv/stop_words/*.txt'
sw_file_list = [file[:] for file in glob.glob(sw_path)]

univ_pattern = r"[가-힣a-zA-Z]{2,}대학교?"
major_pattern = r"^([가-힣]{1,10})(전공|학과|학부)+"
id_pattern = r'^([가-힣]{3,8})?-?([0-9]{2,4})[-(]?학[)-]?([0-9]{2,8})$'
# date_pattern = r'^((19[0-9][0-9]|20\d{2}|202/)[-년\s\\.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s\\.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1])[일\\.]?)?$ '
# date_pattern = r'^([가-힣]+)?(((19|20)\d{2}|202\/)[\-년\s\.]?[\s]?)((0?[0-9]|1[0-2])[-월\s\.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1])[일\.\s])?$'
# date_pattern = r'^((([가-힣]{1,})?\s?(19|20)\d{2}|202\/)[\-년\s\.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s\.][\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1])[일\.\s])?$'
date_pattern = r'^((([가-힣]{1,})?\s?(19|20)\d{2}|202\/)[\-년\s\.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s\.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1]|[0-9])([일\.\s])?)?$'
p_univ = re.compile(univ_pattern)
p_major = re.compile(major_pattern)
p_id = re.compile(id_pattern)
p_date = re.compile(date_pattern)

univ_list = []
major_list = []
name_list = []
id_list = []
date_list = []
date_dict = {}

def character_cleaner(text):
    text = list(map(lambda x: re.sub('[-=+#\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', x), text))
    # text = re.sub('[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
    return text


# 공백제거 replace
def space_cleaner(text):
    # text = [x.replace(' ', '') for x in text]
    text = list(map(lambda x: x.replace(' ', ''), text))
    return text


# 불용어 제거
def stopword_cleaner(text: list) -> list:
    stopwords = []
    for filename in sw_file_list:
        f = open(filename, "r", encoding='UTF-8')
        stopwords += [line[:-1] for line in f.readlines()]
        # print('stopwords', stopwords)
        f.close()
    try:
        text = list(map(lambda x: re.sub("(?<![a-zA-Z가-힣0-9<>])(" + '|'.join(stopwords) + ")(?![a-zA-Z가-힣0-9<>])", "", x), text))
    except Exception as e:
        print('stopwords cleaner occurred error because of ', e)
    # return text[:-1]

    try:
        for w in stopwords:
            for i, t in enumerate(text):
                if w in t:
                    f = t.find(w)
                    if f > 0:
                        t = t[:f] + ' ' + t[f + len(w):]
                    elif f == 0:
                        t = t[f + len(w):]
                    else:
                        pass
                    print(text[i], '>> ', t)

    except Exception as e:
        print(f'{__name__}: {e}')
    return text


def clean_text(data):
    cleaned_data = space_cleaner(data)
    # text = ','.join(cleaned_data)
    text = character_cleaner(cleaned_data)
    text = stopword_cleaner(text)
    print(f'불용어제거 후: {text}')
    return text


# def name_match(datas):
#
#     global name_list
#     name_word = ['성명', ' 명 ', ' 성 ', '명', '성']
#     # 정규식 패턴 정의
#     name_pattern = r"[가-힣]{2,4}"
#     p = re.compile(name_pattern)
#     # datas = [datas]
#     print('datas:', datas)
#     for idx, data in enumerate(datas):
#         text = data
#         # cleaned_data = clean_text(data)
#         # print(f"cleaned_data:{cleaned_data}")
#         for idx2, word in enumerate(name_word):
#             if word in data:
#                 print(f'{word} in {data}')
#                 index = datas.index(word)
#                 print(f'index: {index}')
#                 text = datas[index+1]
#                 print(f'find! : {text}')
#                 # print(f"text:{text}")
#                 print(f'break!')
#                 break
#
#
#         name_m = p.search(text)
#         if name_m:
#             print('이름:', name_m.group())
#             name = name_m.group()
#             name_list.append(name)
#         else:
#             print('pattern does not match')
#
#     name_list = list(set(name_list))
#     # datas = list(itertools.chain.from_iterable(datas))
#     return datas



def name_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 사람 이름과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    print("이름 찾는중...")
    global name_list
    for i in text:
        result = m.parse(i).split('\n')
        result = [a.split('\t') for a in result[:-2]]
        result = [a[0] if a[1].split(',')[1] == '인명' else '' for a in result]

        for j in result:
            if len(j) > 0:
                name_list.append(j)

    name_list = list(set(name_list))
    # print(f"name :  {name_list}")
    if len(name_list) > 0:
        print(f"이름을 찾았습니다. {name_list}\n")
    else:
        print(f"이름 정보를 찾지 못했습니다.")

    return text


def university_match(text: list) -> list:
    # a = p_univ.match(text)
    # print('match:', a)
    # l = p_univ.findall(text)
    # print('univ match: ', l)
    # univ_list.append(l)
    # print('university list', l)
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 대학교명과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 match 메소드에서도 사용해야 함)
    """
    print("학교이름 찾는중...")
    global univ_list
    l = list(map(lambda x: p_univ.match(x), text))

    # ocr로 검출된 학교명이 실제 학교명일 경우 리스트에 담아서 반환
    univ_list = [u.group() for u in l if (u is not None and u.group() in education)]
    
    # 실제학교명이 담겨있으면 중복제거 과정만 수행
    # 실제 학교명이 아니라면 univ_list에 아무것도 담겨있지 않기 때문에
    # ocr로 검출된 내용과 실제 학교리스트를 비교하여 유사한 학교이름으로
    # 가장 유사한 학교이름을 univ_list에 담도록 한다.
    # print('univ_l', univ_list)
    if univ_list:
        # 중복제거
        univ_list = list(set(univ_list))
        
    else:
        # print(f'else univ_list : {univ_list}')
        ## jamo 비교
        tmp = [u.group() for u in l if u is not None]
        max = 0
        max_edu = ''
        for edu in education:
            for t in tmp:
                edu_sum, edu_split = get_jamo_uni(edu)
                t_sum, t_split = get_jamo_uni(t)

                edu_split = list(itertools.chain.from_iterable(edu_split))
                t_split = list(itertools.chain.from_iterable(t_split))

                if len(edu_split) == len(t_split):
                    print(f"{edu}: {edu_split}\n{t}: {t_split}")

                    t1 = np.array(jamo_to_unicode(*edu_split))
                    t2 = np.array(jamo_to_unicode(*t_split))
                    # print(f"{edu} : {t1}\n{t}: {t2}\n")
                    same_count = sum(t1==t2)

                    if max < same_count:
                        max = same_count
                        max_edu = edu

        univ_list.append(max_edu)
    if len(univ_list) > 0:
        print(f"학교를 찾았습니다. {univ_list}\n")
    else:
        print(f"학교 정보를 찾지 못했습니다.\n")
    return text

def id_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 유저를 특징할 수 있는 학위명(ex.서울대2021(학)1234) 과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    print("학위번호 찾는중...")
    l = list(map(lambda x: p_id.match(x), text))
    global id_list
    # l = p_id.findall(text)
    # id_list.append(l)
    for i in range(len(l)):
        if l[i] is not None:
            # print(university_list[i].group(), university_list[i].span())

            # 한글을 영어로 변환
            # ex. 서울 -> seoul
            # v = transliter.translit(l[i].group())
            # print(f'변환 결과: {v}')
            id_list.append(l[i].group())

    if len(id_list) > 0:
        print(f"학위번호를 찾았습니다. {id_list}\n")
    else:
        print(f"학위번호를 찾지 못했습니다.\n")
    return text


def major_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 전공명과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    print("전공을 찾는중...")
    # print(f"\n\n학교리스트: {univ_list}\n\n")
    l = list(map(lambda x: p_major.match(x), text))
    global major_list
    # l = p_major.findall(text)
    # major_list.append(l)
    # print('major match', l)
    for i in range(len(l)):
        if l[i] is not None:
            major_list.append(l[i].group())

    if len(major_list) > 0:
        if univ_list:
            sql = "select distinct 학과명 from pdftest.major_list where 학교명 = '" + univ_list[0] + "' order by 학과명 asc"
            major_db = db.select(sql)['학과명'].tolist()
            # print('db 조회 결과: ', major_db)
            major = 0
            for m in major_db:
                for c in major_list:
                    s = SequenceMatcher(None, c, m).ratio()
                    if s > 0.5:
                        # print('유사도 0.5 이상 학과 >', m, s)
                        if c == m or (c in m) or (m in c):
                            major = m

                    # if max < s:
                    #     max_univ = i
                    #     max = s

        print(f"전공을 찾았습니다. {major}\n")
        major_list = [major]
    else:
        print("전공을 찾지 못했습니다.\n")
    return text


def date_match(text: list) -> list:
    """
    :param text:
    :return:
    """
    print("날짜를 찾는중...")
    date = ''
    l = list(map(lambda x: p_date.match(x) if len(x) > 0 else None, text))
    # print(f'날짜패턴 일치 후보 : {l}')
    global date_dict
    date_cdd = []
    for i in range(len(l)):
        if l[i] is not None and len(l[i].group()) > 0:
            d = l[i].group()
            if l[i].group() == '202/년':
                d = l[i].group().replace('/', '1')
            date_cdd.append(d)
    tmp = []
    # print('date_cdd:', date_cdd)
    year_flag = False
    for i in range(len(date_cdd) - 2):
        # print(f'date_cdd[{i}] : {date_cdd[i]}')
        if i >= len(date_cdd):
            break

        if len(date_cdd[i]) >= 4:
            date = date_cdd[i]
            year_flag = True

        print(date_cdd[i], year_flag)
        # if date_cdd[i].find('년') > 0 and (date_cdd[i].find('년') != len(date_cdd[i]) - 1):
        #     print('?ㅁㄴㅇㅁㄴㅇ:', date_cdd[i])
        #     date += ' ' + date_cdd[i+1]
        if year_flag and len(date_cdd[i+1]) < 4:
            print('월일찾기')
            date += ' ' + date_cdd[i+1] + ' ' + date_cdd[i+2]
            year_flag = False

        tmp.append(date)
    date_cdd = sorted(list(set(tmp)))
    date_keys = ['birth_dt', 'graduation_dt', 'certification_dt']
    date_dict = {key: date_cdd[i] for i, key in enumerate(date_keys)}

    t = list(map(lambda x: date_dict[x].replace('. ', '.'), date_keys))
    t = list(map(lambda x: x.replace('-', '.').replace('. ', '.').replace(' ', '.'), t))
    date_cdd = list(map(lambda x: x.replace('년', '').replace('월', '').replace('일', ''), t))
    date_dict = {key: date_cdd[i] for i, key in enumerate(date_keys)}

    if len(date_dict) > 0:
        print(f"날짜를 찾았습니다. {date_dict}\n")
    else:
        print("날짜를 찾지 못했습니다.\n")

    return text



func_list = [
    ('text', clean_text),
    ('university', university_match),
    ('major', major_match),
    ('id', id_match),
    ('name', name_match),
    ('date', date_match),
]

def list_to_dic(l, l_user):
    """
    
    :param l: 이 모듈에서 사용하고 있는 match함수의 리스트
    :param l_user: 사용자가 사용하길 원하는 match함수의 리스트
    :return: 사용자가 원하는 match 함수를 dict 형태로 반환
    """
    cleaning_dic = OrderedDict()
    for k, v in l:
        if k in l_user:
            cleaning_dic[k] = v

    return cleaning_dic


class Matcher():
    def __enter__(self):
        logger.info("Matcher object is created")
        return self

    def __init__(self, clean_list):
        print('List of match function : \"{}\"\n'.format(", ".join([x[0] for x in func_list])))
        self.clean_list = clean_list
        self.cleaning_dic_cus = list_to_dic(func_list, clean_list)

    def match(self, text: list):
        """
        :param text: ocr로 추출된 내용
        :return: 사용자가 선언한 match 메소드들을 모두 수행하여 학교, 학과, 이름, 학위번호, 날짜정보를
                추출 후 반환
        """
        for func_clean in self.cleaning_dic_cus.values():
            text = func_clean(text)

        # print(f'major_list, {major_list}\nuniv list: {univ_list}\nname list: {name_list}\nld list: {id_list}\ndate list: {date_dict}')
        return text, major_list, univ_list, name_list, id_list, date_dict


    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Matcher object is destroyed")