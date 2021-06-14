import os
import re


def universty_name_match(text: str) -> list:
    """
    :param text:
    :return: word including university name
    """

    pattern = r'^[가-힣]{2,7}대학?교?'
    p = re.compile(pattern)
    result = list(map(lambda x: p.match(x), text))
    print(f'match list >', result)

    return result


def major_match(text: str) -> list:
    """
    :param text:
    :return: word including major
    """

    major_list = []
    pattern = r'^([가-힣]{1,10})(전공|학과|과|학부)'
    p = re.compile(pattern)
    result = list(map(lambda x: p.match(x), text))
    print(f'match list >', result)
    return result


education_list = ['서울대','연세대학교','고려대학교','서울사이버대학교','서울과학기술대학교','경기대학교','경북대학교','홍익대학교','건국대학','숭실대학','동국대','강릉원주대']
major_list = ['국어국문학과', '문예창작과', '컴퓨터인터넷응용학부', '컴퓨터응용엔지니어링', '멀티미디어영상정보전공', '게임과', '스마트IT콘텐츠전공', '컴퓨터융합공학과', '행정경제학과', '경제학부']
result1 = universty_name_match(education_list)
result2 = major_match(major_list)