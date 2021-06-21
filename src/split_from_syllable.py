# -*- coding: utf-8 -*-

from src.jamo_custom import split_syllable_char

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
                        # -1 is 'None'
                        tmp.append(-1)
                r.append(tmp)
            result.append(r)
    return result
