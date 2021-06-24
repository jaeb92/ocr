import os
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

logger = set_logger()
m = MeCab.Tagger()
syn_path = r'../synonym/syn_education.csv'
education_path = r'../res/csv/result.csv'
education = pd.read_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig')['education'].tolist()
syn_file_list = [file[:] for file in glob.glob(syn_path)]
transliter = Transliter(academic)


# print('syn file list', syn_file_list)
# univ_pattern = r"[가-힣a-zA-Z]{2,}대학교?"
univ_pattern = r"[가-힣a-zA-Z]{2,}대학교?"
major_pattern = r'^([가-힣]{1,10})(전공|학과|학부)$'
id_pattern = r'^([가-힣]{3,8})?-?([0-9]{2,4})[-(]?학[)-]?([0-9]{2,8})$'
# date_pattern = r'^(19[0-9][0-9]|20\d{2})[-년 ][ ]?(0?[0-9]|1[0-2])[-월 ][ ]?(0?[1-9]|[1-2][0-9]|3[0-1])[일]?$'
date_pattern = r'^((19[0-9][0-9]|20\d{2}|202/)[-년\s\\.]?[\s]?)?((0?[0-9]|1[0-2])[-월\s\\.]?[\s]?)?((0?[1-9]|[1-2][0-9]|3[0-1])[일\\.]?)?$'
# year_pattern = r'^(19[0-9][0-9]|20\d{2})[-년]?'
# month_pattern = r''

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

# def name_match(text: str) -> str:
#     """
#     :param text: ocr 추출 내용
#         ocr 추출내용중에서 사람 이름과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
#     :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
#     """
#     # for i in text:
#     result = m.parse(text).split('\n')
#     result = [a.split('\t') for a in result[:-2]]
#     l = []
#     for a in result:
#         if(a[1].split(',')[1] == '인명'):
#             l.append(a[0])
#
#     # l = [a[0] if a[1].split(',')[1] == '인명' else '' for a in result]
#     print('name match: ', l)
#     name_list.append(l)
#         # for j in result:
#         #     if len(j) > 0:
#         #         name_list.append(j)
#
#     return text
def name_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 사람 이름과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
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
        print(f'else univ_list : {univ_list}')
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
                    # print(f"{edu}: {edu_split}\n{t}: {t_split}")

                    t1 = np.array(jamo_to_unicode(*edu_split))
                    t2 = np.array(jamo_to_unicode(*t_split))
                    print(f"{edu} : {t1}\n{t}: {t2}\n")
                    same_count = sum(t1==t2)

                    if max < same_count:
                        max = same_count
                        max_edu = edu

        univ_list.append(max_edu)

    return text

def id_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 유저를 특징할 수 있는 학위명(ex.서울대2021(학)1234) 과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
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

    return text


def major_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 전공명과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    l = list(map(lambda x: p_major.match(x), text))
    global major_list
    # l = p_major.findall(text)
    # major_list.append(l)
    # print('major match', l)
    for i in range(len(l)):
        if l[i] is not None:
            major_list.append(l[i].group())

    return text


def date_match(text: list) -> list:
    """
    :param text:
    :return:
    """

    l = list(map(lambda x: p_date.match(x), text))
    global date_list, date_dict
    date_cdd = []
    for i in range(len(l)):
        if l[i] is not None:
            d = l[i].group()
            if l[i].group() == '202/년':
                d = l[i].group().replace('/', '1')
            date_cdd.append(d)
    tmp = []
    for i in range(len(date_cdd)):
        if i >= len(date_cdd):
            break

        if len(date_cdd[i]) >= 4:
            date = date_cdd[i]
            year_flag = True
            if year_flag and len(date_cdd[i+1]) < 4:
                date += ' ' + date_cdd[i+1] + ' ' + date_cdd[i+2]

        tmp.append(date)

    date_cdd = sorted(list(set(tmp)))
    print('date: ', date_cdd)
    date_keys = ['birth_dt', 'graduation_dt', 'certification_dt']
    date_dict = {key: date_cdd[i] for i, key in enumerate(date_keys)}

    # for key, value in tmp_dict.items():
    #     date_dict = {}
    #     date_dict[key] = value
    #     date_list.append(date_dict)

    print('\ndate_dict:', date_dict)
    # if len(date_list) < 1:
    return text

def synonym_cleaner(text: str) -> str:

    lines = []
    for file in syn_file_list:
        f = open(file, "r", encoding='UTF-8-SIG')
        lines += f.readlines()
        f.close()

    lines = list(map(lambda x: x[:-1].split(","), lines))
    lines = [
        (line[0], "(" + "|".join(list(filter(lambda x: len(x) > 0, line[1:]))) + ")")
        for line in lines]
    lines = lines[1:]
    result = []

    for word_rep, regex in lines:
        # print(word_rep, regex)
        # print(type(word_rep), type(regex))
        for t in text:
            t = re.sub(regex, word_rep, t)
            result.append(t)
    # print('result', result)

    return result

func_list = [
    ('university', university_match),
    ('major', major_match),
    ('id', id_match),
    ('synonym', synonym_cleaner),
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
        :param text: ocr로 추출된 내용의 리스트 
        :return: 사용자가 선언한 match 리스트를 모두 수행하고 추출된 각 리스트들
        """
        print('text:', text)
        for func_clean in self.cleaning_dic_cus.values():
            text = func_clean(text)

        # print(f'major_list, {major_list}\nuniv list: {univ_list}\nname list: {name_list}\nld list: {id_list}\ndate list: {date_list}')
        # logger.info(f'\nmajor_list, {major_list}, \nuniv list:, {univ_list},\nname list: , {name_list},\nld list: {id_list}\n')
        return text, major_list, univ_list, name_list, id_list, date_dict


    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Matcher object is destroyed")