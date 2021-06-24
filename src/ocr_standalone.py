import cv2
import os
import numpy as np
import argparse
import time
from easyocr import Reader
import datetime
from utils import get_file_list, move_file, make_new_name
from log_config import set_logger

from ocr_matcher import Matcher

"""
USAGE:
    COMMAND LINE: python ocr_standalone.py -i [image path] -l [ocr language (default: en,ko)] -g [the number of over 0, default -1]
"""

def str_from_img(IN_PATH, OUT_PATH):
    """
    in 폴더의 이미지를 OCR 추출하여 내용을 텍스트파일로 저장하고
    완료된 이미지파일은 파일명을 새로운 아이디로 바꾼 후 out 폴더로 이동시킨다.

    :param IN_PATH: 이미지 경로 
    :param OUT_PATH: ocr 추출 텍스트 파일 저장 경로
    :return: None
    """
    logger = set_logger()
    start = time.time()
    logger.info(f"ocr start time : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"IN_PATH : {IN_PATH}")
    logger.info(f"OUT_PATH: {OUT_PATH}")

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

    # 경로의 이미지 파일들을 가져온다.
    file_list = get_file_list(IN_PATH)

    logger.info(f"file list: {file_list}")
    for file in file_list:
        # time log each files
        file_start_time = time.time()
        file_name = os.path.basename(file)
        print(f'{file_name} start ocr\'ing {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        new_file_name = make_new_name(file_name)

        logger.info(f'file_name: {file_name}')
        logger.info(f'new_file_name: {new_file_name}')
        # save_file_name = file_name.split('.')[0] + '.txt'

        # open file
        # ff = np.fromfile(args["image"], np.uint8) # when run with command line
        ff = np.fromfile(file, np.uint8) # when run with IDE
        image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)

        # make image 4 times bigger than orginal one, using linear interpolation
        image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

        print("[INFO] OCR'ing input image...")

        # default ocr gpu mode( under 0 is using only cpu, over 0 is using gpu )
        gpu = -1

        # default ocr languages
        lang = ['ko', 'en']
        # reader = Reader(lang_list=args["langs"], gpu=args["gpu"] > 0, recognizer='Transformer') # when run with command line
        reader = Reader(lang_list=lang, gpu=gpu, recognizer='Transformer')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        results = reader.readtext(gray)
        contents = []
        for word in results:
            contents.append(word[1].replace('\t', '').replace(':', ' ').replace(' ', ''))

        OCR_SAVE_NAME = os.path.splitext(new_file_name)[0] + '.txt'
        OCR_SAVE_PATH = r'../out/ocr_result/jol/'

        # OCR결과 파일 저장할 경로가 존재하지 않으면 경로 생성
        if not os.path.exists(os.path.join(OCR_SAVE_PATH)):
            print('ocr 저장 경로 없음')
            os.mkdir(os.path.join(OCR_SAVE_PATH))
            print(f'경로 생성됨 >> {os.path.join(OCR_SAVE_PATH)}')

        # OCR 결과 파일로 저장
        with open(os.path.join(OCR_SAVE_PATH, OCR_SAVE_NAME), 'w', encoding='utf-8') as f:
            f.write(str(contents))

        # 원본파일 경로와 옮길 경로를 파라미터로 전달

        t = move_file(file, OUT_PATH, new_file_name)

        logger.info(f"new file name : {t}")

        file_end_time = time.time()
        file_running_time = file_end_time - file_start_time
        file_running_time = str(datetime.timedelta(seconds=file_running_time))
        print(f'{file_name} end ocr\'ing {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        logger.info(f"{file_name} OCR'ing takes {file_running_time} seconds")

    end = time.time()
    running_time = end - start
    running_time = str(datetime.timedelta(seconds=running_time))
    logger.info(f"ocr end time : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"ocr total running time: {running_time} seconds")



# 한성대학교 데이터를 먼저 처리중

# 졸업증명서 FILE PATH
IN_JOL_PATH = r'../res/img/in/png_han_jol/'
OUT_JOL_PATH = r'../res/img/out/png_han_jol/'

# 성적증명서 FILE PATH
IN_SUNG_PATH = r'../res/img/in/png_han_sung/'
OUT_SUNG_PATH = r'../res/img/out/png_han_sung/'

# TEST PATH
IN_TEST_PATH = r'../test/res/img/in/'
OUT_TEST_PATH = r'../test/res/img/out/'


str_from_img(IN_TEST_PATH, OUT_TEST_PATH)
