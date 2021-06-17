from ocr_matcher_test_str_ver import Matcher
import pandas as pd
from difflib import SequenceMatcher
from split_from_syllable import get_split_from_syllable, get_unicode
from jamo import h2j, j2hcj
from vector_test import get_distance
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
    print('x2:', x2)

    return x2


def get_context_from_out():
    try:
        with open('../out/ocr.txt', 'r', encoding='utf-8') as f:
            # 문자열 형태의 리스트를 eval함수를 사용하여 list 객체로 변환
            contents = eval(f.read())
        education = pd.read_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig')['education'].tolist()

    except:
        raise FileNotFoundError

    tmp = []
    # 온전한 대학교명이 존재하면 아래가 가능
    with Matcher(['name', 'university', 'major', 'id']) as matcher:
        text, major_list, univ_list, name_list, id_list = matcher.match(contents)

        for i in univ_list:
            for j in education:
                if i.startswith(j):
                    tmp.append(i)
                    break
            univ_list.remove(i)
            continue
    # print('tmp:', tmp)

    # if len(tmp) > 0:
    #     univ_list = tmp
    # else:
        # 온전한 대학교명이 존재하지 않은 경우 education에서 가장 가까운 대학교명을 찾아 반환.
        # 가변인자 - 리스트 변수에 *(asterisk)를 붙여서 전달하면 리스트가 unpacking되어 전달된다. (미리 unpacking하여 사용가능)
        # 리스트요소 개수에 맞춰 수행됨
        print('find here >> ', education)
        print('target:', univ_list)

        compare_list = []

        # if 완전히 일치하는 대학명이 존재하면 그대로 반환
        # 그렇지 않으면 벡터계산하여 가장 유사한 대학교명을 반환

        for origin in education:
            for target in univ_list:
                ratio = SequenceMatcher(None, target, origin).ratio()
                if ratio >= 0.5 and (len(origin) == len(target)):
                    compare_list.append(origin)

        print('complist:', compare_list)
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
        print(f'm: {m}\nindex: {min_index}')
        print(''.join(univ_list), ' >>> ', compare_list[min_index])
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