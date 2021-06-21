import os.path
from ocr_matcher import Matcher
import pandas as pd
from difflib import SequenceMatcher
from utils import get_split_from_syllable, get_unicode
from jamo import h2j, j2hcj
from distance_vector import get_distance
from log_config import set_logger
import json

import numpy as np
def jamo_test(*args):
    HANGUL_INDEX = 12593

    # print('args:', args)
    jamo = []

    for i in args:
        jamo.append(j2hcj(h2j(i)))
    x = []
    x2 = []

    for i in range(len(jamo)):
        y = []

        total = 0
        for j in range(len(jamo[i])):
            total += int(ord(jamo[i][j]) % HANGUL_INDEX)
            y.append(ord(jamo[i][j]) % HANGUL_INDEX)  # 자,모음의 유니코드가 12593 ~ 12643이므로 가장 작은 수인 12593으로 모듈러 연산을 수행 후 처리


        x.append(y)
        x2.append(total)
            # print(ord(jamo[i][j]))
        # print(type(jamo[i]))
    # print(jamo)
    # print(x)
    # print(y)
    # print('x2:', x2)

    return x2


def get_context_from_out(path):
    # file open try - except
    target = path
    print(f"'{os.path.basename(path)}'에서 정보 추출중...\n")
    try:
        # with open('../out/ocr_result/graduation/ocr.txt', 'r', encoding='utf-8') as f:
        with open(path, 'r', encoding='utf-8') as f:
            # 문자열 형태의 리스트를 eval함수를 사용하여 list 객체로 변환
            contents = eval(f.read())

        # 전체 대학교 리스트 오픈
        education = pd.read_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig')['education'].tolist()

    except:
        raise FileNotFoundError


    tmp = []
    result_dict = {}

    with Matcher(['name', 'university', 'major', 'id']) as matcher:
        text, major_list, univ_list, name_list, id_list = matcher.match(contents)

        print(f"전공 후보: {major_list}")
        print(f"대학교 후보: {univ_list}")
        print(f"이름 후보: {name_list}")
        print(f"아이디 후보: {id_list}")

        # for i in univ_list:
        #     for j in education:
        #         if i.startswith(j):
        #             tmp.append(i)
        #             break
        #     univ_list.remove(i)
        #     continue
        # print('tmp:', tmp)

        # if len(tmp) > 0:
        #     univ_list = tmp
        # else:
        # 온전한 대학교명이 존재하지 않은 경우 education에서 가장 가까운 대학교명을 찾아 반환.
        # 가변인자 - 리스트 변수에 *(asterisk)를 붙여서 전달하면 리스트가 unpacking되어 전달된다. (미리 unpacking하여 사용가능)
        # 리스트요소 개수에 맞춰 수행됨
        # print('find here >> ', education)
        # print('target:', univ_list)

        compare_list = []

        # if 완전히 일치하는 대학명이 존재하면 그대로 반환
        # 그렇지 않으면 벡터계산하여 가장 유사한 대학교명을 반환

        for origin in education:
            for target in univ_list:
                ratio = SequenceMatcher(None, target, origin).ratio()
                print("target :", target)
                print("origin :", origin)
                print("ratio :", ratio)
                if ratio >= 0.3 and (len(origin) == len(target)):
                    compare_list.append(origin)

        print('compare list:', compare_list)
        result = []
        for c in compare_list:
            for target in univ_list:
                # target_jamo_sum = jamo_test(*test_target)
                # origin_jamo_sum = jamo_test(*test_origin)
                target_jamo_sum = jamo_test(target)
                origin_jamo_sum = jamo_test(c)
                # print(f'target: {target}, jamo sum {target_jamo_sum}')
                # print(f'origin: {c}, jamo sum {origin_jamo_sum}')
                # print('origin:', origin_jamo_sum)
                for i in target_jamo_sum:
                    for j in origin_jamo_sum:
                        # print(i, j, abs(i-j))
                        result.append(abs(i - j))

        a = get_split_from_syllable(*compare_list)
        b = get_split_from_syllable(*univ_list)

        c = get_unicode(a)
        d = get_unicode(b)

        m, min_index = get_distance(c, d)
        print(f'계산된 벡터 : {m}\n최소값의 인덱스: {min_index}')
        # print(f'm: {m}\nindex: {min_index}')

        try:
            print(''.join(univ_list), ' >>> ', compare_list[min_index], '\n')
        except Exception as e:
            logger = set_logger()
            logger.info(f"raised exception: {e}")
            # print(f'====raised exception====\n{e}')

        result_sub_dict = {}

        result_sub_dict['university'] = univ_list
        result_sub_dict['major'] = major_list
        result_sub_dict['name'] = name_list

        result_dict[id_list[0]] = result_sub_dict


        with open(r'../out/dict_result/result.json', 'a', encoding='utf-8-sig') as f:
            json.dump(result_dict, f, ensure_ascii=False)

        del univ_list[:]
        del major_list[:]
        del name_list[:]
        del id_list[:]


# ======================================== 대학교 비교부분(수정중) =======================================
# e = jamo_compare(*education)
# u = jamo_compare(*univ_list)
# # print('e', e)
# # print('u', u)
# result = []
# for i in u:
#     for j in e:
#         result.append(abs(i-j))
#         # print(i, j)
# print(result)
# print(min(result), education[np.argmin(result)])
# print(univ_list, id_list, major_list, name_list)