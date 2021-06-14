import os
import cv2
from numpy.lib.function_base import interp
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pprint
import time
from easyocr import Reader
from ocr_matcher2 import Matcher

##########################
#### 클리너 형태로 수정 ####
##########################


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()
start = time.time()

#
matcher = Matcher([
    'name',
    'university',
    'major',
    'id',
])
matcher.match(['민원번호', '제', '05-H-221호', '학번 ', '198915097', '성적증명서', '성', '명', '김주철', '대', '학', '생명과학부', '학위증서번호', '제075105호', '성', '별', '남', '학부|학과/전공', '운용생화학선공', '학위등록번호', '2012(학)0819\
', '생년월일', '1968년', '4월', '2일', '제1전공용웅생화학전공', '학위명', '제1전공이학사', '입학년월일', '1989년', '3월', '2일', '제2전공', '제2전공', '졸업년월일', '1996년', '2월22일', '제3전공', '제3전공', '조기졸업', '연계연합\
전공', '연계연합전공', '부전', '공', '교과목명', '학점성적', '교과목명', '학점성적', '교과목명', '(학점|성적', '1992년도1학기', '1993년도2학기', '1995년도2학기', '선교', '생활스포츠', '2', '전필', '생화학및실험1', '4', 'C+', '전선',
 '분자생리학', '3', 'B', '선교', '생물의원리', '2', '3', '취득학점 ', '19누', '계 ', '74', '취득학점 ', '9누', '계 ', '140', '교', '화학및실험1', '3', 'B+', '평점평균 ', '3.00평점평균 ', '3.09', '평점평균 ', '3.33평점평균 ', '3.05',
 '짓', '교', '생물학및실험1', '3', '백분위 ', '84.0백분위 ', '84.9', '백분위 ', '87.3백분위 ', '84.5', '교', '수학및연습1', '3', '필교', '철학의이해', '2', '8', '1994년도1학기', '구분', '학점', '평점평균', '백분울', '필교', '영어1',
 '2', '선교', '인간과신소재', '2', 'A', '(4.50만점)', '(100만점)', '필교', '한국어문2', '2', '전선', '효소학', '3', 'B+', '전공', '70', '2.87', '82.7', '전선', '기기분석학', '3', 'C+', '취득학점 ', '19누', '계 ', '19', '교양', '70',
 '3.23', '86.3', '전선', '3', '평점평균 ', '3.02평점평균 ', '3.02', '선', '생체고분자화학및실험', '8', '백분위 ', '84.2백분위 ', '84.2', '전', '다전공', '0', '0.00', '0.0', '필', '생화학및실험2', '4', 'C', '1992년도2학기', '취득학점\
 ', '19누', '계 ', '93', '부전공', '0.00', '0.0', '전필', '생물화학', '3', 'C+', '평점평균 ', '2.68평점평균 ', '3.01', '옆객', '0.00', '0.0', '지교', '화학및실험2', '3', 'A+', '백분위', '80.8백분위 ', '84.1', '교', '수학및연습2', '3\
', 'B', '교직', '0.00', '0.0', '짓', '교', '생물학및실험2', '3', 'B+', '1994년도2학기', '필교', '독어', '2', 'C+', '선교', '전기와그이용', '2', 'A', '기타', '0.00', '0.0', '필교', '영어2', '2', 'B+', '선교', '경제성장과공해', '2', '\
D+', '합계', '140', '3.05', '84.5', '필교', '한국어문1', '2', 'B', '선교', '화학의원리', '2', 'B', '전선', '생화학실험학', '3', 'D+', '취득학점 ', '18누', '계 ', '37', '전선', '호르국생화학및실험', '4', 'B+', '평점평균 ', '3.25평점\
평균 ', '3.13', '전필', '생체물리화학', '3', 'A', '백분위 ', '86.5', '백분위 ', '85.3', '전필', '분자생물학', '3', 'C+', '1993년도1학기', '취득학점 ', '19누', '계 ', '112', '선교', '인간생활과동물', '2', '평점평균 ', '2.89평점평균 '
, '2.99', '선교', '경제학입문', '2', '탓', '백분위 ', '82.9백분위 ', '83.9', '교', '물질의세계', '2', '뿐', '교', '심리학의이해', '2', 'B', '1995년도1학기', '선', '생명과학개론', '3', 'C+', '선교', '계절스포츠', '2', '전필', '생체유\
기화학', '3', 'B+', '선교', '과학과철학', '931', '2', '전필', '유기화학및실험', '4', 'B+', '교', '자원과에너지', '2', ';', '선', '과학영어', '3', '취득학점 ', '18누', '계 ', '55', '평점평균 ', '3.11', '평점평균 ', '3.12', '물', '선'
, '영양생화학', '3', '선', '임상생화학', '3', 'C+', '백분위 ', '85.1', '백분위 ', '85.2', '필', '유전생화학및실험', '해', '4', 'C+', '1993년도2학기', '취득학점 ', '19누', '계 ', '131', '선교', '레저스포츠', '2', 'A+', '평점평균 ', '\
3.31평점평균 ', '3.03', '선교', '국악의이해', '2', 'B+', '백분위 ', '87.1', '백분위 ', '84.3', '선교', '지구과학', '2', 'C', '1995년도2학기', '선교', '식생활과건강', '2', 'C+', '전선', '세포생화학', '3', 'A', '선교', '인간과환경', '\
2', 'A', '전필', '미생물학및실험', '4', 'C+', '선교', '행정학입문', '2', 'A', '선교', '미학개론', '2', 'C+', "'성적등급", 'A+ 4.5,A 4.0,B+ 3.5', 'B 3.0,C+ 2.5,C 2.0,D+ 1.5', 'D 1.0', '*E=영어강의,F=프랑스어강의,G=독일어강의,C=중국어\
강의,H=히브리어강의,J=일분어강의,', 'R=러시아어강의,|=유학생대상강의,W=취득학점-기', '**[드림학기', '과목명 드림학기설계]한학기동안수업대신자기주도프로직트수행결과루토대로학점올인정받는교육과정임', '**증명서상전공은재학중에는전과나\
다전공포기등으로변경월수있으면,졸업년월일이후발급분에한하여확정되는사항임', '위의사실올증명함', '2021년', '5월', '28일', '건국대학교', '교', '무활빵활', '#본증명서는인터넷으로발급한증명서로서,웬민원센터(WWWwebminwoncom)예서원본화인\
문서번호틀통해원본대조가가능(발급후180일간).*제출용은칼라프린터출력올권장.', '킬기물_히다라임실협h', '도'])
# matcher.match(['한밭대-2005-학-2029', '민원번호', '성적', '증명서', '제WB-PREVIEW', '호', '06974서울특별시동작구특석로84', '(전화', '02)820-6035,6036', '명', '권오주', '생년', '월일 ', '1987.', '1.', '15', '학위명)', '학', '번 20052876', '선', '공', '의과대학의학부','동국대학교'])
# ap = argparse.ArgumentParser()
#
# ap.add_argument("-i", "--image", required=True,
#                 help="path to input image to be OCR'd")
# # ap.add_argument("-l", "--langs", type=str, default="en",
# #                 help="comma separated list of languages to OCR")
# ap.add_argument("-g", "--gpu", type=int, default=-1,
#                 help="whether or not GPU should be used")
# args = vars(ap.parse_args())
#
# # break the input languages into a comma separated list
# # langs = args["langs"].split(",")
# # print("[INFO] OCR'ing with the following languages: {}".format(langs))
# # load the input image from disk
#
# ff = np.fromfile(args["image"], np.uint8)
# image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
# image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
# # image = cv2.imread(args["image"])
#
# # print(type(image))
# # print(image)
# # OCR the input image using EasyOCR
# print("[INFO] OCR'ing input image...")
# reader = Reader(['ko', 'en'], gpu=args["gpu"] > 0, recognizer='Transformer')
# gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
# results = reader.readtext(gray)
# # print(results)
# # print(f'resutls: {results}')
# contents = []
# for word in results:
#     contents.append(word[1].replace('\t', '').replace(' ', '').replace(':', ' '))
#     # print(results[i][1].replace('\t', '').replace(' ', ''), end=' ')
# # print(' '.join(contents))
#
# # print('contents:', contents)
# univ_m = matcher.university_match(contents)
# name_m = matcher.name_match(contents)
# major_m = matcher.major_match(contents)
# print(f'\n\nuniv match : {univ_m}\nname match: {name_m}\nmajor match: {major_m}')
# print(results[0])
# loop over the results

# =================================
# object bounding box
# for (bbox, text, prob) in results:
#     text = text.replace(' ', '')
#     if matcher.university_match(text):
#         # display the OCR'd text and associated probability
#         print(text, len(text))
        # print("[INFO] {:.4f}: {}".format(prob, text.replace(' ', '')))
    # unpack the bounding box
    # (tl, tr, br, bl) = bbox
    # tl = (int(tl[0]), int(tl[1]))
    # tr = (int(tr[0]), int(tr[1]))
    # br = (int(br[0]), int(br[1]))
    # bl = (int(bl[0]), int(bl[1]))
    # # cleanup the text and draw the box surrounding the text along
    # # with the OCR'd text itself
    # text = cleanup_text(text)
    # cv2.rectangle(image, tl, br, (0, 255, 0), 2)
    # cv2.putText(image, text, (tl[0], tl[1] - 10),
    # cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
end = time.time()
running_time = end - start
print(f'running time : {running_time}')

# show the output image
# image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
# cv2.imshow("Image", image)
# cv2.waitKey(0)

# try:
#     from PIL import Image
# except:
#     import Image

# def get_file_list(path):
#     """
#     디렉토리 내의 모든 파일 경로 가져오기
#     """
#     files = []
#     for root, dirname, filename in os.walk(path):
#         for file in filename:
#             if file:
#                 files.append(os.path.join(root, file))

#     return files

# def erosion_dilation(gray_img): 
#     height, width = gray_img.shape 
#     out = np.zeros((height + 2, width + 2), dtype=np.uint8) 
#     out[1:1 + height, 1:1+width] = gray.copy() 
#     erode = np.zeros_like(gray_img) 
#     dilate = np.zeros_like(gray_img) 
#     for i in range(height): 
#         for j in range(width): 
#             temp = out[i:i+3, j:j+3] 
#             erode[i][j] = np.min(temp) 
#             dilate[i][j] = np.max(temp) 

#     # mask
#     ar = np.array(
#         [
#             [1, 1, 1], 
#             [1, 1, 1], 
#             [1, 1, 1]
#         ]
#     ) 
#     erosion = cv2.erode(gray, ar) 
#     dilation = cv2.dilate(gray, ar)


# def imshow(title, image):
#     print(f'title: {title}\nimage shape: {image.shape}\nimage shape len: {len(image.shape)}')
#     plt.title(title)    

#     if len(image.shape) == 3:
#         plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#     else :
#         plt.imshow(image, cmap="gray")
#     plt.show()

# IMG_PATH = '.\\res\\img'
# TEMP_PATH = '.\\res\\img\한양사_성_1.pdf.jpg'
# file_path_list = get_file_list(IMG_PATH)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"
# config = ('-l kor+eng --oem 3 --psm 4')
# # print(file_path_list)
# i = 0
# # # for file_path in file_path_list:
# ff = np.fromfile(TEMP_PATH, np.uint8)
# ff = np.fromfile(file_path_list[0], np.uint8)
# origin = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)

# img_linear = cv2.resize(origin, None, fx=4.0, fy=4.0, interpolation=cv2.INTER_LINEAR)
# img_cubic = cv2.resize(origin, None, fx=4.0, fy=4.0, interpolation=cv2.INTER_CUBIC)

# img_linear_gray = cv2.cvtColor(img_linear, cv2.COLOR_RGB2GRAY)
# img_cubic_gray = cv2.cvtColor(img_cubic, cv2.COLOR_RGB2GRAY)

# linear_ret, linear_mask = cv2.threshold(img_linear_gray, 125, 255, cv2.THRESH_BINARY)
# cubic_ret, cubic_mask = cv2.threshold(img_cubic_gray, 125, 255, cv2.THRESH_BINARY)
# kernel = np.ones((5,5), np.uint8)
# erode = cv2.erode(img_linear, kernel=kernel)
# dilate = cv2.dilate(erode, kernel=kernel)
# # dst = cv2.filter2D(image, -1, sharpening_1)

# sharpening_2 = np.array([[-1, -1, -1, -1, -1],
#                          [-1, 2, 2, 2, -1],
#                          [-1, 2, 9, 2, -1],
#                          [-1, 2, 2, 2, -1],
#                          [-1, -1, -1, -1, -1]]) / 9.0

# sharpen = cv2.filter2D(erode, -1, kernel=sharpening_2)
# print(f'linear_ret {linear_ret}')
# # linear_mask_rev = 255 - linear_mask

# # laplacian = cv2.Laplacian(linear_mask_rev, -1)

# imshow('sharpen', sharpen)
# # imshow('bin', np.hstack((linear_mask, cubic_mask)))

# print(linear_mask.shape)
# print(cubic_mask.shape)

# text = pytesseract.image_to_string(sharpen, config=config)
# print(f'{text}')
# imshow('img_linear', img_linear)
# contents = text.replace('\n\n', ' ')
# contents = text.replace('\n\n', ' ')
# h = '학 위' in contents
# print(text.replace('\n\n', ' '))

# print('대 학 교' in text.replace('\n\n', ' '))
# dhk_index = contents.find('대 학 교') 
# print(text[dhk_index:dhk_index+6])
# imshow('img', np.hstack((linear_mask, cubic_mask)))
# imshow('image', np.hstack((img_cubic, img_linear)))


# cv2.imshow('img', np.stack((img_linear, img_cubic)))

# if cv2.waitKey(0) == ord('q'):
# cv2.destroyAllWindows()

# print(img_linear.shape) 
# cv2.imshow('img', img)
# if cv2.waitKey(0) == ord('q'):
#     cv2.destroyAllWindows()


# while True:
#     img = cv2.imread(file_path_list[i], cv2.IMREAD_COLOR)
#     print(img)
#     cv2.imshow('img', img)

#     if cv2.waitKey(0) == ord('q'):
#         break

#     i += 1
