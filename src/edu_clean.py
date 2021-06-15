import pandas as pd
import re

univ_pattern = r'^[가-힣a-zA-Z]{2,8}대?학?교?'
p_univ = re.compile(univ_pattern)

df = pd.read_csv('./res/csv/education_list.csv', sep=',', encoding='utf-8-sig')
a = list(map(lambda x: p
l = df['학교명'].tolist()_univ.match(x), l))
result = [v.group() if v is not None else '' for v in a]
result = sorted(set(result))
print(result)

# 리스트 -> 데이터프레임 -> csv파일 저장
d = pd.DataFrame(result).to_csv('./result.csv', sep=',', encoding='utf-8-sig')
