import re
import os
import glob
import hanja
import MeCab
from bs4 import BeautifulSoup


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

"""
경로 변경 필요
"""
syn_path = r'D:/email_ai/preprocess/synonym/*.csv'
sw_path = r'D:/email_ai/preprocess/stop_words/*.txt'
syn_file_list = [file[:] for file in glob.glob(syn_path)]
sw_file_list = [file[:] for file in glob.glob(sw_path)]
m = MeCab.Tagger()

print('syn_file_list :', syn_file_list)
print('sw_file_list :', sw_file_list)

########################################################################################################################
# 기능; 
#   1. html 형식 문서에서 하이퍼링크가 걸린 텍스트의 경우, 텍스트 내용을 링크주소로 매핑
#   2. html 형식 문서에서 텍스트만 추출
# 인풋; (문자열) html 형식 문서
# 출력; 하이퍼링크 변환 및 텍스트 추출이 완료된 문자열
########################################################################################################################
def html_cleaner(html):
    bs = BeautifulSoup(html, 'html.parser')
    for script in bs(["script", "style"]):
        script.extract()

        # 링크의 경우 보여지는 텍스트가 실제 링크주소가 되도록 변경
    # for a in bs.find_all('a'):
    #     try:
    #         a.string = a.attrs['href']
    #     except:
    #         # print(a)
    #         pass

    return bs.get_text(" ", strip=True)


########################################################################################################################
# 기능: html 문법에서 스페이스를 대체하는 문자들 및 탭을 스페이스로 대체 
########################################################################################################################
def space_cleaner(text):
    text = text.replace('&nbsp', ' ').replace('&amp', ' ').replace('\t', ' ')
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    return text


########################################################################################################################
# 기능; 입력 문자열에 계좌 정보가 포함되었을 경우  <account> 토큰으로 마스킹
########################################################################################################################
def account_cleaner(text):
    return re.sub('(\d{3,6}-\d{2,6}-\d{2,7})(-\d{1,6})?', ' <account> ', text)




########################################################################################################################
# 기능: 메일 작성시 자동 포함되는 스크립트 제거
########################################################################################################################
def rm_script(text):
    script = [
        "This email and any attachments are confidential and may also be privileged. If you are not the intended recipient, please delete all copies and notify the sender immediately. You may wish to refer to the incorporation details of Standard Chartered PLC, Standard Chartered Bank and their subsidiaries at https://www.sc.com/en/our-locations. Please refer to https://www.sc.com/en/privacy-policy/ for Standard Chartered Bank’s Privacy Policy.",
        "This message and its attachments may contain confidential information, and they are intended to be viewed or used by only the individuals specified in the message.  If you have received this message in an error from the sender, please contact the sender immediately to notify the error and delete all of the message and its copies.  It is prohibited to view, use, make public and/or distribute part or whole of this message without written permission.",
        "상기 메시지와 첨부화일 내에는 비밀정보가 포함되어 있을 수 있으며 , 지정된 수신자에 한하여 조회 및 사용될 수 있습니다 . 만약 송신자의 실수로 인하여 상기 메시지를 수신하였다면 , 송신자에게 메시지를 반송해 주시고 , 원본 메시지와 모든 사본을 폐기해 주시기 바랍니다 . 상기 메시지의 전체 또는 일부에 대해 무단 열람 , 사용 , 공개 , 배포하는 것은 금지되어 있습니다 . \( 주 \) LG CNS.",
        "The information contained in this message may be privileged, confidential and protected from disclosure. If the reader of this message is not the intended recipient, or an employee or agent responsible for delivering this message to the intended recipient, you are hereby notified that any dissemination, distribution or copying of this communication is strictly prohibited. If you have received this communication in error, please notify your representative immediately and delete this message from your computer. Thank you.",
        'NOTICE : This email and any attachments to it may be confidential and are intended solely for the use of the individual to whom it is addressed. If you have received this communication in error, please contact the sender immediately, and delete this communication from any computer or network system. LG CNS America Inc.',
        "Office Mobile The foregoing message is sent by Corporation and is intended to be confidential You should not forward this message without permission from the sender If you received this message in error please delete it"
        "This mail message may contain confidential and or privileged information If you are not an addressee or otherwise authorized to receive this message you should not use copy disclose or take any action based on this mail or any information contained in the message If you have received this material in error please advise the sender immediately by reply mail and delete this message",
        "COPYRIGHT \(C\) 20\d\d LG CNS.ALL RIGHTS RESERVED. UCESSDI@LGCNS.COM"
    ]

    script = ['\s*'.join(s.lower().split(" ")) for s in script]

    for s in script:
        text = re.sub(s, ' ', text)

    script2 = [ "confidential this mail is intended solely for the named addressee and may contain information that is privileged confidential or otherwise protected under applicable law any unauthorized dissemination distribution copying or use of the information contained in this communication is strictly prohibited if you have received this communication in error please notify the sender by email and delete this communication immediately 상기 메세지 지정 수신인 위한 부정 경쟁 방지 영업 비밀 보호 관한 법률 포함 관련 법령 따라 보호 대상 영업 비밀 기밀 정보 포함 메세지 포함 정보 전부 일부 무단 공개 배포 복사 사용 금지 됩니다 메세지 전송 경우 발신인 알려 메세지 삭제 바랍니다"]
    script2 = ['\s*'.join(s.lower().split(" ")) for s in script2]

    for s in script2:
        text = re.sub(s, ' ', text)
    return text


########################################################################################################################
# 기능: 문자열에 요일 정보가 포함되었을 경우 <date>로 마스킹
########################################################################################################################
def dayofweek_cleaner(text):
    dayofweek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"] 

    for p in dayofweek:
        text = re.sub(p, " <day_of_week> ", text)

    return text


########################################################################################################################
# 기능: 문자열에 날짜 정보가 포함되었을 경우 <date>로 마스킹
########################################################################################################################
def date_cleaner(text):
    date_ps = [re.compile('(20)?\d\d[\s/.-]?(0?[1-9]|1[0-2])[\s/.-]?([0-2]\d|3[0-1])[\s/.-](\d{1,2}:\d{1,2})'),
               re.compile('(20)?\d\d[\s/.-](0?[1-9]|1[0-2])[\s/.-]([0-2]\d|3[0-1])'),
               re.compile('(20)?\d\d(0[1-9]|1[0-2])([0-2]\d|3[0-1])'),
               re.compile('(0?[1-9]|1[0-2])[\s/.-]([0-2]\d|3[0-1])[\s/.-]\d{2}'),
               re.compile('(0?[1-9]|1[0-2])[/.]([0-2]\d|3[0-1])'),
               re.compile('(20|19)\d{2}\s*년'),
               re.compile('(2|1)\d\s*년'),
               re.compile('(0?[1-9]|1[0-2])\s*월'),
               re.compile('([0-2]\d|3[0-1])\s*일')]

    for p in date_ps:
        text = p.sub(" <date> ", text)

    return text

########################################################################################################################
# 기능: 문자열에 시간 정보가 포함되었을 경우 <time>로 마스킹
########################################################################################################################
def time_cleaner(text):
    time_ps = [re.compile('[^\d][0-2]?(\d:[0-5]){1,2}\d(pm|am)?'),
               re.compile('[^\d][0-2]?\d(pm|am)'),
               re.compile('[^\d][0-2]?\d(시)'),
               re.compile('[^\d][0-5]\d(분)')
               ]

    for p in time_ps:
        text = p.sub(' <time> ', text)
    return text


########################################################################################################################
# 기능; 입력 문자열에 이메일 주소가 포함되었을 경우  cns/ cnspartner/ normal 로 나누어 마스킹
########################################################################################################################
def email_cleaner(text):
    # email 3종류 - cns/ cnspartner/ normal
    email_ps = [
        (re.compile('(?:^|(?<=[^\\w@.)]))(?:[\\w+-](?:\\.(?!\\.))?)*?[\\w+-]@lgcns.com(?:$|(?=\\b))'), ' <cns_email> '),
        (re.compile('(?:^|(?<=[^\\w@.)]))(?:[\\w+-](?:\\.(?!\\.))?)*?[\\w+-]@cnspartner.com(?:$|(?=\\b))'),
         ' <cnspartner_email> '),
        (re.compile(
            '(?:^|(?<=[^\\w@.)]))(?:[\\w+-](?:\\.(?!\\.))?)*?[\\w+-]@(?:\\w-?)*?\\w+(?:\\.(?:[a-z]{2,})){1,3}(?:$|(?=\\b))'),
         ' <email> ')]

    for p, v in email_ps:
        text = p.sub(v, text)
    return text




########################################################################################################################
# 기능; 입력 문자열에  url이 포함되었을 경우  url_file/ url 로 나누어 마스킹
########################################################################################################################
def url_cleaner(text):
    # url 4종류 -
    bs = BeautifulSoup(text, 'html.parser')
    for script in bs(["script", "style"]):
        script.extract()

        # 링크의 경우 보여지는 텍스트가 실제 링크주소가 되도록 변경
    for a in bs.find_all('a'):
        try:
            a.string = a.attrs['href']
        except:
            # print(a)
            pass

    text = bs.get_text(" ", strip=True)
    url_list = [('drive.google', ' <url_file> '), ('bigfile.mail', ' <url_file> '), ('cloud.naver', ' <url_file> '),
                (' ', ' <url> ')]
    for u, t in url_list[:-1]:
        text = re.sub('(?:https?:\\/\\/(?:www\\.|(?!www))' + u[:-1] + '[^\\s\\.]+\\.[^\\s]{2,}|www\\.' +
                      u[:-1] + '[^\\s]+\\.[^\\s]{2,})',
                      t, text)
    # if 'bigfile' in text:# bigfile은 종류가 많아서 따로 처리
    if 'download' in text:
        text += ' <url_file> '

    for u, t in url_list[-1:]:
        text = re.sub('(?:https?:\\/\\/(?:www\\.|(?!www))' + u[:-1] + '[^\\s\\.]+\\.[^\\s]{2,}|www\\.' +
                      u[:-1] + '[^\\s]+\\.[^\\s]{2,})',
                      t, text)
    return text


########################################################################################################################
# 기능; 입력 문자열에 한자가 포함되었을 경우 한글 음독으로 치환
########################################################################################################################
def hanja_sub(text):
    return hanja.translate(text, 'substitution')


########################################################################################################################
# 기능; 입력 문자열에 한자가 포함되었을 경우 <hanja> 로 마스킹
########################################################################################################################
def hanja_cleaner(text):
    return re.sub("[一-龥]", '<hanja>', text)


########################################################################################################################
# 기능; 입력 문자열에 휴대전화 번호가 포함되었을 경우 <phone> 로 마스킹
########################################################################################################################
def phone_cleaner(text):
    phone_ps = [re.compile('(?<![0-9])(\+\()?(8\d)[\s\).-]?\d{2,3}[\s.-]?\d{4}[\s.-]?\d{4}(?![0-9])'),
                re.compile('(?<![0-9])0(2|[3-6][1-5]|1\d)[\s.-]?\d{3,4}[\s.-]?\d{4}(?![0-9])'),
                re.compile('(?<![0-9])(0(2|[3-6][1-5]))?(1577|1544|1644|1600|1566|1688|1666|1599)[\s.-]?\d{4}(?![0-9])')]
    for ps in phone_ps:
        text = ps.sub(' <phone> ', text)

    return text



# 성능 테스트, 중복 제외

########################################################################################################################
# 기능; ekphrasis 패키지를 이용해 'url', 'time', 'date' 정보 마스킹
# (커스텀 함수들과 중복사항이 존재해 체크 필요)
########################################################################################################################
def ekp_cleaner(text):
    from ekphrasis.classes.preprocessor import TextPreProcessor

    text_processor = TextPreProcessor(
        # terms that will be normalized
        normalize=['url', 'time', 'date'],  # 'number' 대체 안함
        fix_html=True,  # fix HTML tokens (&nbsp 등)
        unpack_hashtags=False,  # perform word segmentation on hashtags
        unpack_contractions=False,  # Unpack contractions (can't -> can not)
        spell_correct_elong=False,  # spell correction for elongated words
        tokenizer=None,  # mecab_tokenizer,
        mode='fast',
    )

    return text_processor.pre_process_doc(text)


########################################################################################################################
########################################################################################################################
def elongated_cleaner(text: str) -> str:
    """
    기능; 3번 이상 중복된 문자가 나타날 경우 2번으로 치환

    Args:
        text:

    Returns:

    """
    # 가가가가가나다 -> 가가나다
    cleaned = text[0:2]
    for i in range(len(text) - 2):
        if text[i] == text[i + 1] and text[i + 1] == text[i + 2]:
            continue
        else:
            cleaned += text[i + 2]
    return cleaned


########################################################################################################################
#
########################################################################################################################
def name_cleaner(text: str) -> str:
    """
    기능; 입력 문자열을 형태소 분석한 결과 이름 정보가 포함되었을 경우 <name> 로 마스킹
    (tokenizer 에 동일 기능 포함되어 있음)
    Args:
        text: 이름 마스킹되기 전 문서

    Returns: 이름 마스킹 된 문서

    """
    result = m.parse(text).split('\n')
    result = [a.split('\t') for a in result[:-2]]
    result = ['<name>' if a[1].split(',')[1] == '인명' else a[0] for a in result]

    return " ".join(result)


########################################################################################################################

########################################################################################################################
def stopword_cleaner(text: str) -> str:
    """
    입력 문자열에 포함된 불용어 제거
    불용어 사전 위치: project_path/preprocess/stop_words/
    불용어 사전 포맷:
    - 확장자: .txt
    - 설명: 줄바꿈으로 구분된 단어들 (공백 없음)
    - 예시: 다람쥐\n공룡\n토끼\n
    Args:
        text: 불용어 제거 전 문서

    Returns: 불용어 제거된 문서

    """
    stopwords = []
    for filename in sw_file_list:
        f = open(filename, "r", encoding='UTF-8')
        stopwords += [line[:-1] for line in f.readlines()]
        f.close()
    # print('stopword cnt:::::::' , len(stopwords),ROOT_DIR)
    text = " " + text + " "

    try:
        text = re.sub("(?<![a-z가-힣0-9<>])(|" + '|'.join(stopwords) + "|)(?![a-z가-힣0-9<>])", "", text)
    except Exception as e:
        print('stopwords cleaner occurred error because of', e)

    return text[:-1]


########################################################################################################################
# 입력 문자열에 포함된 유사어 치환
# 유사어 사전 위치: project_path/preprocess/synonym/
# 유사어 사전 포맷:
#   - 확장자: .csv
#   - 설명: comma로 구분된 단어들, 같은 줄일 떄 서로 유사어, 맨 첫 단어가 대표어
#   - 예시: 대표어,유사어,유사어1,유사어2
########################################################################################################################
def synonym_cleaner(text):
    lines = []
    for file in syn_file_list:
        f = open(file, "r", encoding = 'UTF-8')
        lines += f.readlines()
        f.close()

    lines = list(map(lambda x: x[:-1].split(","), lines))
    lines = [
        (line[0], "(" + "|".join(list(filter(lambda x: len(x) > 0, line[1:]))) + ")")
        for line in lines]
    lines = lines[1:]

    for word_rep, regex in lines:
        text = re.sub(regex, word_rep, text)

    return text



########################################################################################################################
# 기능; 문자, 숫자, 마침표, &, <> 제외 문자열에 포함된 모든 특수문자 제거
########################################################################################################################
def specialch_cleaner(text):
    return re.sub('[^a-zA-Z0-9가-힣\\.&<>_]+', ' ', text)


########################################################################################################################된
# 기능; 길이가 min_length 이상인 단어만 보존
########################################################################################################################
def minlength_cleaner(text):
    min_length = 1
    text = text.split(' ')
    text = list(filter(lambda x: len(x) > min_length, text))

    return ' '.join(text)


########################################################################################################################
# 기능: 문자열에 파일 정보가 포함되었을 경우 이미지/압축파일/소스코드/문서로 나누어 마스킹
# (파일명에 공백 포함시 마스킹이 제대로 안 될 수 있음)
########################################################################################################################
def file_cleaner(text):
    file_ps = [
        (re.compile('([^ ;])+\.(jpg|jpeg|png)( |;)'), ' <image_file> '),
        (re.compile('([^ ;])+\.(zip|7z|tar)( |;)'), ' <compressed_file> '),
        (re.compile('([^ ;])+\.(py|java|c|pynb)( |;)'), ' <sourcecode_file> '),
        (re.compile('([^ ;])+\.(hwp|docx|xlsx|ppt|csv|pdf|xls|pptx)( |;)'), ' <document_file> ')
    ]
    for p, v in file_ps:
        text = p.sub(v, text)
    return text


########################################################################################################################
# 기능:
#   1. Mecab 형태소 분석기를 이용해 토크나이징 및 형태소 분석
#   2. (optional) 원하는 형태소를 가진 단어만 포함
#   3. (optional) 이름 정보 마스킹
#  인풋;
#   text: 대상 문자열
#   rm_stop: (optional, default=True) True일 경우 원하는 형태소를 가진 단어만 포함
#   tagging: (optional, default=False) True일 경우 이름 정보 마스킹
########################################################################################################################
def mecab_tokenizer(text, rm_stop=True, tagging=False):
    result = m.parse(text).split('\n')
    result = [a.split('\t') for a in result[:-2]]

    if rm_stop:
        result = [a for a in result if (a[1][0] not in 'JESMI' or a[1][:2] in ['SL', 'SN'])]  # 일단 다 살리고 나중에 처리하기
    # result = [a for a in result if (a[1][0] not in 'JESMI')]
    if tagging:
        result = ['<name>T' if a[1].split(',')[1] == '인명' else a[0] + a[1][0] for a in result]
    else:
        result = ['<name>' if a[1].split(',')[1] == '인명' else a[0] for a in result]

    return " ".join(result)


from collections import OrderedDict

fucn_list = [('html', html_cleaner),
             ('space', space_cleaner),
             ('script', rm_script),
             ('email', email_cleaner),
             ('file', file_cleaner),
             ('url', url_cleaner),
             ('phone', phone_cleaner),
             ('date', date_cleaner),
             ('time', time_cleaner),
             ('dayofweek', dayofweek_cleaner),
             ('account', account_cleaner),
             ('hanja', hanja_sub),
             ('ekp', ekp_cleaner),
             ('specialch', specialch_cleaner),             
             ('synonym', synonym_cleaner),
             ('name', name_cleaner),             
             ('elongated', elongated_cleaner),
             ('tokenize', mecab_tokenizer),
             ('stopword', stopword_cleaner),
             ('minlength', minlength_cleaner),
             ]


def list_to_dic(l, l_user):
    cleaning_dic = OrderedDict()
    for k, v in l:
        if k in l_user:
            cleaning_dic[k] = v
    return cleaning_dic


class Cleaner():
    def __init__(self, clean_list):
        #print('List of cleaning function : {}'.format(", ".join([x[0] for x in fucn_list])))
        self.clean_list = clean_list
        self.cleaning_dic_cus = list_to_dic(fucn_list, clean_list)

    def cleaning(self, text, lower=True):
        if text != text:
            return text

        if lower:
            text = text.lower()

        for func_clean in self.cleaning_dic_cus.values():
            text = func_clean(text)

        return text