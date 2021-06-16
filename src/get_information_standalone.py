from ocr_matcher_test_str_ver import Matcher
import pandas as pd

try:
    with open('../out/ocr.txt', 'r', encoding='utf-8') as f:
        # 문자열 형태의 리스트를 eval함수를 사용하여 list 객체로 변환
        contents = eval(f.read())
    education = pd.read_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig')['education'].tolist()

except:
    raise FileNotFoundError

matcher = Matcher([
    'name',
    'university',
    'major',
    'id',
])
text, major_list, univ_list, name_list, id_list = matcher.match(contents)

tmp = []
# 온전한 대학교명이 존재하면 아래가 가능
for i in univ_list:
    for j in education:
        if i.startswith(j):
            tmp.append(i)

# 온전한 대학교명이 존재하지 않은 경우 education에서 가장 가까운 대학교명을 찾아 반환.
univ_list = tmp
print(univ_list, id_list, major_list, name_list)