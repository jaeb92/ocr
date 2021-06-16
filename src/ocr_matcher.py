import os
import glob
import MeCab
import re
from collections import OrderedDict


m = MeCab.Tagger()

univ_pattern = r'^[가-힣]{2,7}대학?교'
major_pattern = r'^(.)+([가-힣]{1,10})(전공|학과|학부)$'
id_pattern = r'^([가-힣]{3,8})?-?([0-9]{2,4})[-(]?학[)-]?([0-9]{2,8})$'

p_univ = re.compile(univ_pattern)
p_major = re.compile(major_pattern)
p_id = re.compile(id_pattern)

univ_list = []
major_list = []
name_list = []
id_list = []

def name_match(text: list) -> list:
    for i in text:
        result = m.parse(i).split('\n')
        result = [a.split('\t') for a in result[:-2]]
        result = [a[0] if a[1].split(',')[1] == '인명' else '' for a in result]

        for j in result:
            if len(j) > 0:
                name_list.append(j)

    # result = list(map(lambda x: m.parse(x).split('\n'), text))

    # result = m.parse(text).split('\n')
    # print('r', result)
    # for i in range(len(result)):
    #     print(result[i])
        # result = [a.split('\t') for a in result[:-2]]
    # print('a', result)
    # result = [a if a[1].split(',')[1] == '인명' else a[0] for a in result]
    # print(type(result), result)
    # return result

# def name_match(text: list) -> list:
#     """
#     입력 문자열을 형태소 분석한 결과 이름 정보가 포함되어 있을 경우 <name>으로 마스킹
#     """
#     result = map(lambda x: self.m.parse(x).split('\n'), text)
#     result = []
#     for i in range(len(text)):
#         result.append(self.m.parse(text[i]).split('\n'))
#     print('1', result)
#     # for r in result:
#     #     print(r)
#     # for i in range(len(result)):
#     #     print(result[i])
#     # print('result:', result)
#     # for i in range(len(result)):
#     #      print(result[i].split['\t'])
#     result = self.m.parse(text).split('\n')
#     result = [a.split('\t') for a in result[:-2]]
#     result = ['<name>' if a[1].split(',')[1] == '인명' else a[0] for a in result]
#
#     print(result)
    # return result



def university_match(text: list) -> list:
    """
    :param text:
    :return: word including university name
    """
    l = list(map(lambda x: p_univ.match(x), text))
    # print('university list', l)
    for i in range(len(l)):
        if l[i] is not None:
            # print(university_list[i].group(), university_list[i].span())
            univ_list.append(l[i].group())

    # print('ae univ list:', univ_list)

    #
    # for i in range(len(university_list)):
    #     r = text.find(university_list[i])
    #     text = re.sub(r'^[가-힣]{2,7}대학?교?', '*' * len(university_list[i]), text)
    #     university_name = university_list[i]
    #     # print(text[r:len(result[i])])
    #     print('r', r)
    #     # text = text.replace(reg_univ.sub(text, '*'*len(result[i])), "")
    # # text = reg_univ.subn(text[result])
    # # result = list(map(lambda x: p.match(x), text))
    return text

def id_match(text: list) -> list:
    l = list(map(lambda x: p_id.match(x), text))

    # print('university list', l)
    for i in range(len(l)):
        if l[i] is not None:
            # print(university_list[i].group(), university_list[i].span())
            id_list.append(l[i].group())

    return text


def major_match(text: list) -> list:
    """
    :param text:
    :return: word including major
    """
    l = list(map(lambda x: p_major.match(x), text))
    # print('major_list', l)
    for i in range(len(l)):
        # print(major_list[i])
        if l[i] is not None:
            # print(major_list[i].group(), major_list[i].span())
            major_list.append(l[i].group())

    # print('ab major list', major_list)
    # # major_list = p_major.findall(text)
    # print('major list', major_list)
    # for i in range(len(major_list)):
    #     r = text.find(major_list[i])
    #     text = re.sub(r'^(.)+([가-힣]{1,10})(전공|학과|학부)', '*' * len(major_list[i]), text)
    # pattern = r'^([가-힣]{1,10})(전공|학과|과|학부)'
    # print(t for t in text)
    # result = list(map(lambda x: p.match(x), text))
    return text

func_list = [
    ('university', university_match),
    ('major', major_match),
    ('id', id_match),
    ('name', name_match),
]

def list_to_dic(l, l_user):
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
        for func_clean in self.cleaning_dic_cus.values():
            text = func_clean(text)

        print('major_list', major_list, '\nuniv list:', univ_list, '\nname list: ', name_list, '\nld list: ', id_list)
        return text
