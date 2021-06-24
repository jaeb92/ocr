import os
import datetime
import random
import shutil
import json
import pprint
from jamo_custom import split_syllable_char
from jamo import h2j, j2hcj


def make_number_two_digits(digit: str) -> str:
    if len(str(digit)) < 2:
        if digit != 0:
            digit = '0' + str(digit)

    return digit


def make_new_name(file):
    """
    파일 경로를 입력받아 새로운 이름을 만들어서 반환함
    :param path: 파일의 parent 경로
    :param file: 파일명
    :return:
    """
    # micro 초까지 동일한 경우가 있어서 4자리 정수 추가로 생성해서 붙임
    rand = str(random.randint(1000, 9999))
    change = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
    file_ext = os.path.splitext(file)[1]
    new_name = change+''+rand+''+file_ext
    # new_file_path = os.path.join(path, new_name)
    # file_path = os.path.join(path, file)
    return new_name


def save_json(path: str, dictionary: dict, id: str) -> None:
    """
    json 파일의 경로와 저장할 데이터, 그리고 이를 식별할 키를 파라미터로 입력받고
    이를 json파일에 새롭게 쓰도록 한다.

    :param path: json 파일 경로(ex. d1/d2/d3/sample.json 
    :param dictionary: ocr 검출 결과 파일에서 뽑아낸 학교, 학과, 식별자(학위번호), 이름, 날짜 데이터
    :param id: dictionary를 식별할 키 (이미지 파일의 새로운 파일명, ex. 20210623_1404505664938731)
    :return: None
    """

    # 파일 read
    with open(path, 'r+', encoding='utf-8-sig') as f:
        j = f.read()
        json_obj = json.loads(j)
        json_obj['result'][id] = dictionary
        json_obj['last_modified'] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # pprint.pprint(json_obj)

    # 새로운 내용 저장
    with open(path, 'w+', encoding='utf-8-sig') as f:
        f.write(json.dumps(json_obj, ensure_ascii=False))


# def save_file(path: str, obj: object, if_exists :str='append', plus: bool=False) -> None:
#     """
#     :param path:
#         save path
#     :param if_exists:
#         1) append -> 기존 내용 뒤에 이어 씀
#         2) write -> 새로운 내용을 씀
#         3) read -> 파일 내용을 읽음
#
#     :param plus:
#         True -> read and write
#         ex a+, w+, r+
#     :return: None
#     """
#
#     if if_exists == 'append':
#         file_mode = 'a'
#     elif if_exists == 'write':
#         file_mode = 'w'
#     elif if_exists == 'read':
#         file_mode = 'r'
#
#     if plus:
#         file_mode += '+'
#
#     print(f'path: {path}')
#     filename = os.path.basename(path)
#     ext = filename.split('.')[1]
#     print(f'ext: {ext}')

def move_file(path: str, out_path: str, new_file_name: str) -> str:
    """
    파일 또는 폴더의 경로를 인자로 받아 해당 파일 또는 폴더 안의 모든 파일들에 대해
    out폴더로 이동시킨다.

    :param path: file's list will be changed the name
    :return: new file name ( ex. 20211225_122531[1234](현재날짜_시간[임의의 정수4자리] )
    """

    new_name = os.path.join(os.path.dirname(path), new_file_name)
    go_to = os.path.join(out_path, os.path.basename(new_name))
    os.rename(path, new_name)

    # 옮길 디렉토리 없으면 새로 생성
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    shutil.move(new_name, go_to)
    print(f"{os.path.basename(path)} is moved from {os.path.dirname(path)} to {out_path}")

    # 기존파일명과 바뀐파일명 바뀐 시간을 기록
    with open(r'../change_file_name_list.txt', 'a+', encoding='utf-8') as f:
        f.write(str(os.path.basename(path)) + ' --> ' + str(new_file_name) + '\t기록시간: ' + str(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write('\n')

    return new_file_name

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
            syl = [args[i][j]]

            # 대학명에 영어가 들어갈 경우 한글로 바꿔서 초,중,종성을 분리한다.
            if (ord(args[i][j]) >= 65 and ord(args[i][j]) <= 90) or (ord(args[i][j]) >= 97 and ord(args[i][j]) <= 122):
                t = alphabet_to_hangul(args[i][j])
                syl = t

            # 음절을 초,중,종성으로 분리
            for s in syl:
                a.append(split_syllable_char(s))
        r.append(a)
        # print(f'r: {r}')
    return r



def get_unicode(*args):
    _HANGUL_INDEX = 12593

    result = []
    for i in range(len(args)):
        for j in range(len(args[i])):
            r = []
            for k in range(len(args[i][j])):
                tmp = []
                for l in range(len(args[i][j][k])):
                    if args[i][j][k][l] is not None:
                        tmp.append(ord(args[i][j][k][l]) % _HANGUL_INDEX)
                    else:
                        tmp.append(-1) # -1 == 'None'
                r.append(tmp)
            result.append(r)
    return result


def get_jamo_uni(*args):
    _HANGUL_INDEX = 12593

    # print('args:', args)
    jamo = []

    for i in args:
        # print(f'dddd: {i}')
        jamo.append(j2hcj(h2j(i)))
        split_syl = get_split_from_syllable(i)

    x = []
    x2 = []
    # print(f"jamo: {jamo}")
    # print(f"{args}, jamo len: {len(jamo[0])}")
    # print(f'args: {args}')
    # a = get_split_from_syllable2(args)
    # print(f"{a}")
    for i in range(len(jamo)):
        y = []

        total = 0
        for j in range(len(jamo[i])):
            total += int(ord(jamo[i][j]) % _HANGUL_INDEX)
            y.append(ord(jamo[i][j]) % _HANGUL_INDEX)  # 자,모음의 유니코드가 12593 ~ 12643이므로 가장 작은 수인 12593으로 모듈러 연산을 수행 후 처리
        x.append(y)
        x2.append(total)

    return x2, split_syl


def alphabet_to_hangul(syllable):
    char_map = {
        "a": "에이", "b": "비", "c": "씨", 'd': "디",
        "e": "이", "f": "에프", "g": "지", 'h': "에이치",
        "i": "아이", "j": "제이", "k": "케이", 'l': "엘",
        "m": "엠", "n": "엔", "o": "오", 'p': "피",
        "q": "큐", "r": "알", "s": "에스", 't': "티",
        "u": "유", "v": "브이", "w": "더블유", 'x': "엑스",
        "y": "와이", "z": "제트"
    }

    result = [char_map[char.lower()] for char in syllable if char_map[char.lower()]]
    result = ''.join(result)

    return result


def jamo_to_unicode(*args):
    _HANGUL_INDEX = 12593

    result = []
    for syl in args:
        for i, jamo in enumerate(syl):
            if jamo is not None:
                jamo_uni = ord(jamo)
            else:
                jamo_uni = -1

            result.append(jamo_uni % _HANGUL_INDEX)
            # print(jamo, jamo_uni, end=' ')

    return result