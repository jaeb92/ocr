from jamo import h2j, j2hcj
from utils import get_split_from_syllable
import numpy as np


def get_jamo_uni():
    ja = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    mo = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
    a = []
    b = []
    for m in mo:
        a.append(ord(m))
    for j in ja:
        b.append(ord(j))

    mo = sorted(set(mo))
    ja = sorted(set(ja))
    uc = sorted(set(a))
    jc = sorted(set(b))
    # print('moeum:', mo)
    # print('jaeum:', ja)
    # print('mo_uni:', uc)
    # print('ja_uni:', b)

def jamo_compare(*args):
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
            total += int(ord(jamo[i][j]))
            y.append(ord(jamo[i][j]))

            print(jamo[i][j])
        x.append(y)
        x2.append(total)
        # print(ord(jamo[i][j]))
        # print(type(jamo[i]))
    # print(x)
    print('x2:', x2)

    return x2

# ========= test ==============
test_origin = ['서울사회복지대학원대학교']
test_target = ['셔울과학기술대학교']
a = get_split_from_syllable(*test_target)
b = get_split_from_syllable(*test_origin)

print(a)
print(b)
# target_jamo_sum = jamo_compare(*test_target)
# origin_jamo_sum = jamo_compare(*test_origin)
# print('target:', target_jamo_sum)
# print('origin:', origin_jamo_sum)