import os
from jamo_custom import split_syllable_char

def get_file_list(path):
    """
    디렉토리 내의 모든 파일 경로 가져오기
    """
    files = []
    for root, dirname, filename in os.walk(path):
        for file in filename:
            if file:
                files.append(os.path.join(root, file))

    return files


def get_split_from_syllable(*args):
    r = []
    for i in range(len(args)):
        a = []
        for j in range(len(args[i])):
            a.append(split_syllable_char(args[i][j]))
        r.append(a)
    # print(r)
    return r

def get_unicode(*args):
    HANGUL_INDEX = 12593

    result = []
    for i in range(len(args)):
        for j in range(len(args[i])):
            r = []
            for k in range(len(args[i][j])):
                tmp = []
                for l in range(len(args[i][j][k])):
                    if args[i][j][k][l] is not None:
                        tmp.append(ord(args[i][j][k][l]) % HANGUL_INDEX)
                    else:
                        tmp.append(-1) # -1 == 'None'
                r.append(tmp)
            result.append(r)
    # print(f'list = {result}')
    return result