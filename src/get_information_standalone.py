import copy
import os.path
import pprint
from ocr_matcher import Matcher


def get_context_from_out(path):

    """
    :param path: ocr추출 결과 txt파일 
    :return: 학교, 학과, 이름, 식별자, 날짜 dictionary
    """
    # file open try - except

    print(f"'{os.path.basename(path)}'에서 정보 추출중...\n")
    try:
        # with open('../out/ocr_result/graduation/ocr.txt', 'r', encoding='utf-8') as f:
        with open(path, 'r', encoding='utf-8') as f:
            # 문자열 형태의 리스트를 eval함수를 사용하여 list 객체로 변환
            contents = eval(f.read())
            f.close()
    except:
        raise FileNotFoundError


    result_dict = {}

    matcher = Matcher([
        'text',
        'name',
        'university',
        'major',
        'id',
        'date'
    ])
    text, major_list, univ_list, name_list, id_list, date_dict = matcher.match(contents)

    # print(f"전공 : {major_list}")
    # print(f"대학교 : {univ_list}")
    # print(f"이름 : {name_list}")
    # print(f"아이디 : {id_list}")
    # print(f"날짜 : {date_dict}")

    print("전공 =", end='\t')
    pprint.pprint(major_list)
    print("대학 =", end='\t')
    pprint.pprint(univ_list)
    print("이름 =", end='\t')
    pprint.pprint(name_list)
    print("학위명 =", end='\t')
    pprint.pprint(id_list)
    print("날짜 =", end='\t')
    pprint.pprint(date_dict)


    result_dict['university'] = copy.copy(univ_list)
    result_dict['major'] = copy.copy(major_list)
    result_dict['name'] = copy.copy(name_list)
    result_dict['date'] = copy.copy(date_dict)
    result_dict['degree_Number'] = copy.copy(id_list)


    # result_dict[id_list[0]] = result_sub_dict

    del univ_list[:]
    del major_list[:]
    del name_list[:]
    del id_list[:]
    date_dict.clear()

    return result_dict
