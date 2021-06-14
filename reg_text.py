import re
import MeCab
m = MeCab.Tagger()

# text = ["서울대학교", "동국대학교", "가나다라고려대학교"]
# univ_pattern = r'^[가-힣]{2,7}대학?교?'
# p_univ = re.compile(univ_pattern)
# print('문자열: ', text)
# university_list = list(map(lambda x: p_univ.match(x), text))
# for i in range(len(university_list)):
#     print(university_list[i].group(), university_list[i].span())
#     print(university_list[i].start())
#     print(university_list[i].end())
#     print(university_list[i].span())
# for i in range(len(university_list)):
#     print(i, ' ', university_list[i])
l =  ['민원번호', '성적', '증명서', '제WB-PREVIEW', '호', '06974서울특별시동작구특석로84', '(전화', '02)820-6035,6036', '명', '권오주', '생년', '월일 ', '1987.', '1.', '15', '학위명)', '학', '번 20052876', '선', '공', '의과대학의학부', '동국대학교']
s = '황재빈 씨에스리 서울시 마포구 상암동'
t = []
for i in l:
    result = m.parse(i).split('\n')
    result = [a.split('\t') for a in result[:-2]]
    result = [a[0] if a[1].split(',')[1] == '인명' else '' for a in result]
    # result = list, result))
    for j in result:
        if len(j) > 0:
            t.append(j)
    # t.append(j if len(j) > 0 else '' for j in result)
    # for j in result:
print(t)
    #     print(len(j))
    # print(result)
# result = list(map(lambda x: m.parse(x).split('\n'), l))
# print(result)
# for a in result[:-2]:
#     for b in a:
#         result = b.split('\t')
#         for c in result:
#             print(c.split(','))
#             if c[1].split(',') == '인명':
            #     result = c
            # else:
            #     result = ''
            # print(c.split(','))
            # if c[1].split(',')[1] == '인명':
            #     result = c
            # else:
            #     result = c[0]
    # print(result)
# for a in l[:-]:
#     print(a)
# result = [a.split('\t') for a in result[:-2]]
# result = [a if a[1].split(',')[1] == '인명' else a[0] for a in result]

# print(result)