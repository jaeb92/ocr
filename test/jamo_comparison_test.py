from jamo import h2j, j2hcj
import numpy as np
mo = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
a = []
for m in mo:
    a.append(ord(m))

mo = sorted(set(mo))
uc = sorted(set(a))
# print(mo)
# print(uc)



def jamo_test(*args):
    print('args:', args)
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


        x.append(y)
        x2.append(total)
            # print(ord(jamo[i][j]))
        # print(type(jamo[i]))
    # print(x)
    print('x2:', x2)

    return x2


# test_origin = ['서울과학기술대학교','서울교육대학교','서울기독대학교','서울대학교','서울디지털대학교','서울사이버대학교']
# test_target = ['셔울과학기술대학교']
test_origin = ['원광대학교','원광디지털대학교','원광보건대학교','위덕대학교']
test_target = ['대학교']
target_jamo_sum = jamo_test(*test_target)
origin_jamo_sum = jamo_test(*test_origin)
print('target:', target_jamo_sum)
print('origin:', origin_jamo_sum)
result = []
for i in target_jamo_sum:
    for j in origin_jamo_sum:
        result.append(abs(i-j))
print(min(result), test_origin[np.argmin(result)])
# print(abs(target_jamo_sum - origin_jamo_sum))
# for i in range(1, 6):
#     for c in f'jamo{i}':
#         print(f'{jamo{i}}')
#         o.append(ord(c))
#         print(ord(c))
#
# print(o)

# print(j2hcj(h2j(test1)))
# print(j2hcj(h2j(test2)))
# print(j2hcj(h2j(test3)))
# print(j2hcj(h2j(test4)))
# print(j2hcj(h2j(test5)))


# ratio = SequenceMatcher(None, test1, test2).ratio()
# print(ratio)