import pandas as pd
import re

univ_pattern = r'^[가-힣a-zA-Z]{2,}대?학?교?'
p_univ = re.compile(univ_pattern)

df = pd.read_csv('../res/csv/education_list.csv', sep=',', encoding='utf-8-sig')
l = df['학교명'].tolist()
len_l = len(l)
a = list(map(lambda x: p_univ.match(x), l))
result = [v.group() if v is not None else '' for v in a]
result = list(map(lambda x: x.split(' ')[0], result))
result = sorted(set(result))


len_r = len(result)
print('중복제거전 :', len_l)
print('중복제거후 :', len_r)

print(result)

# 리스트 -> 데이터프레임 -> csv파일 저장
d = pd.DataFrame(result, columns=['education']).to_csv('../res/csv/result.csv', sep=',', encoding='utf-8-sig', index=False)
