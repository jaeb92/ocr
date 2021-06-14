import os
import glob
import MeCab
import re
from collections import OrderedDict


class Matcher:
    def __init__(self):
        self.m = MeCab.Tagger()
        # ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
        # print(f'ROOT_DIR : {ROOT_DIR}')

    def name_match(self, text: list) -> str:
        print(__name__)
        """
        입력 문자열을 형태소 분석한 결과 이름 정보가 포함되어 있을 경우 <name>으로 마스킹
        """
        l = []
        for i in range(len(text)):
            l.append(self.m.parse(text[i]).split('\n'))

        for i in range(len(l)):
            for j in range(len(l[i])):
                b = l[i][j].split('\t')
                if len(b) > 1:
                    if b[1].split(',')[1] == '인명':
                        print(b[0])
                        return b[0]

    # def name_match(text: list) -> list:
    #     """
    #     입력 문자열을 형태소 분석한 결과 이름 정보가 포함되어 있을 경우 <name>으로 마스킹
    #     """
    #     result = map(lambda x: self.m.parse(x).split('\n'), text)
    #     result = []
    #     for i in range(len(text)):
    #         result.append(self.m.parse(text[i]).split('\n'))
    #     print('1', result)
    #     # for r in result:
    #     #     print(r)
    #     # for i in range(len(result)):
    #     #     print(result[i])
    #     # print('result:', result)
    #     # for i in range(len(result)):
    #     #      print(result[i].split['\t'])
    #     result = self.m.parse(text).split('\n')
    #     result = [a.split('\t') for a in result[:-2]]
    #     result = ['<name>' if a[1].split(',')[1] == '인명' else a[0] for a in result]
    #
    #     print(result)
        # return result



    def university_match(self, text: list) -> list:
        """
        :param text:
        :return: word including university name
        """
        print('un', text)
        pattern = r'^[가-힣]{2,7}대학?교?'
        p = re.compile(pattern)
        result = list(map(lambda x: p.match(x), text))

        return result


    def major_match(self, text: list) -> list:
        """
        :param text:
        :return: word including major
        """
        major_list = []
        print(text)
        # pattern = r'^([가-힣]{1,10})(전공|학과|과|학부)'
        pattern = r'^(.)+([가-힣]{1,10})(전공|학과|학부)'
        p = re.compile(pattern)
        # print(t for t in text)
        result = list(map(lambda x: p.match(x), text))
        return result


# def list_to_dic(l, l_user):
#     cleaning_dic = OrderedDict()
#     for k, v in l:
#         if k in l_user:
#             cleaning_dic[k] = v
#     return cleaning_dic
#
#
# class Cleaner():
#     def __init__(self, clean_list):
#         #print('List of cleaning function : {}'.format(", ".join([x[0] for x in fucn_list])))
#         self.clean_list = clean_list
#         self.cleaning_dic_cus = list_to_dic(fucn_list, clean_list)
#
#     def cleaning(self, text, lower=True):
#         if text != text:
#             return text
#
#         if lower:
#             text = text.lower()
#
#         for func_clean in self.cleaning_dic_cus.values():
#             text = func_clean(text)
#
#         return text
# education_list = ['서울대','연세대학교','고려대학교','서울사이버대학교','서울과학기술대학교','경기대학교','경북대학교','홍익대학교','건국대학','숭실대학','동국대','강릉원주대']
# major_list = ['국어국문학과', '문예창작과', '컴퓨터인터넷응용학부', '컴퓨터응용엔지니어링', '멀티미디어영상정보전공', '게임과', '스마트IT콘텐츠전공', '컴퓨터융합공학과', '행정경제학과', '경제학부']
# result1 = universty_name_match(education_list)
# result2 = major_match(major_list)
# cleaned_text = name_match(text)
# print(cleaned_text)