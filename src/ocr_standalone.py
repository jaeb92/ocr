import cv2
import os
import numpy as np
import argparse
import time
from easyocr import Reader
from datetime import datetime
from ocr_matcher_test_str_ver import Matcher

"""
USAGE:
    COMMAND LINE: python ocr_standalone.py -i [image path] -l [ocr language (default: en,ko)] -g [the number of over 0, default -1]
"""
def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

start = time.time()

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

# 이미지 경로 수정부분
img_path = r'../res/img/졸업/선문_졸_1.jpg'
# ff = np.fromfile(args["image"], np.uint8) # when run with command line
ff = np.fromfile(img_path, np.uint8) # when run with IDE
image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

print("[INFO] OCR'ing input image...")
gpu = -1
lang = ['ko','en']
# reader = Reader(lang_list=args["langs"], gpu=args["gpu"] > 0, recognizer='Transformer') # when run with command line
reader = Reader(lang_list=lang, gpu=gpu, recognizer='Transformer')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
results = reader.readtext(gray)

contents = []
for word in results:
    contents.append(word[1].replace('\t', '').replace(':', ' ').replace(' ', ''))

print(contents)
with open('../out/ocr.txt', 'w', encoding='utf-8') as f:
    f.write(str(contents))

end = time.time()
running_time = end - start
running_time = str(datetime.timedelta(seconds=running_time))

print(f'running time : {running_time}')