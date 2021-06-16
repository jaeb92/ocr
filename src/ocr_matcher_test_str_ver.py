import os
import glob
import MeCab
import re
from collections import OrderedDict

m = MeCab.Tagger()
syn_path = r'../synonym/syn_education.csv'
syn_file_list = [file[:] for file in glob.glob(syn_path)]
print('syn file list', syn_file_list)
univ_pattern = r"[가-힣a-zA-Z]{2,}대학교?"
major_pattern = r'^(.)+([가-힣]{1,10})(전공|학과|학부)$'
id_pattern = r'^([가-힣]{3,8})?-?([0-9]{2,4})[-(]?학[)-]?([0-9]{2,8})$'

p_univ = re.compile(univ_pattern)
p_major = re.compile(major_pattern)
p_id = re.compile(id_pattern)

univ_list = []
major_list = []
name_list = []
id_list = []

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
    for i in text:
        result = m.parse(i).split('\n')
        result = [a.split('\t') for a in result[:-2]]
        result = [a[0] if a[1].split(',')[1] == '인명' else '' for a in result]

        for j in result:
            if len(j) > 0:
                name_list.append(j)
    return text

def university_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 대학교명과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    l = list(map(lambda x: p_univ.match(x), text))
    # a = p_univ.match(text)
    # print('match:', a)
    # l = p_univ.findall(text)
    # print('univ match: ', l)
    # univ_list.append(l)
    # print('university list', l)
    for i in range(len(l)):
        if l[i] is not None:
            univ_list.append(l[i].group())

    print(univ_list)
    return text

def id_match(text: list) -> list:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 유저를 특징할 수 있는 학위명(ex.서울대2021(학)1234) 과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    l = list(map(lambda x: p_id.match(x), text))
    # l = p_id.findall(text)
    # id_list.append(l)
    # print('id match:', l)
    # print('university list', l)
    for i in range(len(l)):
        if l[i] is not None:
    #         # print(university_list[i].group(), university_list[i].span())
            id_list.append(l[i].group())

    return text


def major_match(text: str) -> str:
    """
    :param text: ocr 추출 내용
        ocr 추출내용중에서 전공명과 매치되는 내용을 리스트에 담아서 최종적으로 반환함.
    :return ocr 추출한 내용을 그대로 반환(다른 메소드에서도 사용해야 함)
    """
    l = list(map(lambda x: p_major.match(x), text))
    # l = p_major.findall(text)
    # major_list.append(l)
    # print('major match', l)
    for i in range(len(l)):
    #     # print(major_list[i])
        if l[i] is not None:
            major_list.append(l[i].group())

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
        print(word_rep, regex)
        print(type(word_rep), type(regex))
        for t in text:
            t = re.sub(regex, word_rep, t)
            result.append(t)
    print('result', result)

    return result

func_list = [
    ('university', university_match),
    ('major', major_match),
    ('id', id_match),
    ('synonym', synonym_cleaner),
    ('name', name_match),
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
    def __init__(self, clean_list):
        print('List of match function : \"{}\"'.format(", ".join([x[0] for x in func_list])))
        self.clean_list = clean_list
        self.cleaning_dic_cus = list_to_dic(func_list, clean_list)

    def match(self, text: list) -> list:
        """
        :param text: ocr로 추출된 내용의 리스트 
        :return: 사용자가 선언한 match 리스트를 모두 수행하고 추출된 각 리스트들
        """
        print('text:', text)
        for func_clean in self.cleaning_dic_cus.values():
            text = func_clean(text)

        print('=========================================================return results=========================================================\n'
              'major_list', major_list, '\nuniv list:', univ_list, '\nname list: ', name_list, '\nld list: ', id_list,
              '\n================================================================================================================================\n')
        return text, major_list, univ_list, name_list, id_list
