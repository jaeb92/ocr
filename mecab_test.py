import re
import glob
import MeCab
import os

m = MeCab.Tagger()

def name_cleaner(text: list) -> str:
    """
    입력 문자열을 형태소 분석한 결과 이름 정보가 포함되어 있을 경우 <name>으로 마스킹
    """
    l = []
    for i in range(len(text)):
        l.append(m.parse(text[i]).split('\n'))

    for i in range(len(l)):
        for j in range(len(l[i])):
            b = l[i][j].split('\t')
            if len(b) > 1:
                if b[1].split(',')[1] == '인명':
                    return b[0]


text = ['졸업증명서', '성', '명 장영환']

a = name_cleaner(text)
print(a)