import cv2
import os
import numpy as np
import argparse
import time
from easyocr import Reader
import datetime
from utils import get_file_list
from ocr_matcher_test_str_ver import Matcher

"""
USAGE:
    COMMAND LINE: python ocr_standalone.py -i [image path] -l [ocr language (default: en,ko)] -g [the number of over 0, default -1]
"""
# def cleanup_text(text):
#     # strip out non-ASCII text so we can draw the text on the image
#     # using OpenCV
#     return "".join([c if ord(c) < 128 else "" for c in text]).strip()

def str_from_img(IN_PATH, OUT_PATH):
    IN_GRADU_PATH = r'../res/img/graduation/'
    IN_SCORE_PATH = r'../res/img/score/'

    OUT_GRADU_PATH = r'../out/ocr_result/graduation/'
    OUT_SCORE_PATH = r'../out/ocr_result/score'

    # =========================== USE BELOW WHEN RUN FILE WITH COMMAND LINE ===========================
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-i", "--image", required=True,
    #                 help="path to input image to be OCR'd")
    # ap.add_argument("-l", "--langs", type=str, default="en,ko",
    #                 help="comma separated list of languages to OCR")
    # ap.add_argument("-g", "--gpu", type=int, default=-1,
    #                 help="whether or not GPU should be used")
    # args = vars(ap.parse_args())
    # =====================================================================================

    file_list = get_file_list(IN_PATH)
    for file in file_list:
        file_name = os.path.basename(file)
        save_file_name = file_name.split('.')[0] + '.txt'

        # open file
        # ff = np.fromfile(args["image"], np.uint8) # when run with command line
        ff = np.fromfile(file, np.uint8) # when run with IDE
        image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
        image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

        print("[INFO] OCR'ing input image...")
        gpu = -1
        lang = ['ko', 'en']
        # reader = Reader(lang_list=args["langs"], gpu=args["gpu"] > 0, recognizer='Transformer') # when run with command line
        reader = Reader(lang_list=lang, gpu=gpu, recognizer='Transformer')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        results = reader.readtext(gray)
        contents = []
        for word in results:
            contents.append(word[1].replace('\t', '').replace(':', ' ').replace(' ', ''))
        #
        # print(contents)

        # with open('../out/ocr.txt', 'w', encoding='utf-8') as f:
        #     f.write(str(contents))

        # 저장할 경로 존재하지 않으면 경로 생성
        if not os.path.exists(os.path.join(OUT_PATH)):
            print('경로 생성함')
            os.mkdir(os.path.join(OUT_PATH))

        # OCR 결과 파일로 저장
        with open(os.path.join(OUT_PATH, save_file_name), 'w', encoding='utf-8') as f:
            f.write(str(contents))


start = time.time()
str_from_img()
end = time.time()
running_time = end - start
running_time = str(datetime.timedelta(seconds=running_time))

print(f'running time : {running_time}')