import cv2
import numpy as np
import argparse
import time
from easyocr import Reader
from ocr_matcher_test_str_ver import Matcher

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

matcher = Matcher([
    'name',
    'university',
    'major',
    'id',
])
start = time.time()
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
# ap.add_argument("-l", "--langs", type=str, default="en",
#                 help="comma separated list of languages to OCR")
ap.add_argument("-g", "--gpu", type=int, default=-1,
                help="whether or not GPU should be used")
args = vars(ap.parse_args())

# 이미지 경로 수정부분
ff = np.fromfile(args["image"], np.uint8)
image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)

print("[INFO] OCR'ing input image...")
reader = Reader(['ko', 'en'], gpu=args["gpu"] > 0, recognizer='Transformer')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
results = reader.readtext(gray)

contents = []
for word in results:
    contents.append(word[1].replace('\t', '').replace(':', ' ').replace(' ', ''))
    # print(results[i][1].replace('\t', '').replace(' ', ''), end=' ')

# contents = ' '.join(contents)
print('contents type: ', type(contents))
# print('contents:', contents)
text, major_list, univ_list, name_list, id_list = matcher.match(contents)
print(major_list, univ_list, name_list, id_list)
# ================================================
# univ_m = matcher.university_match(contents)
# name_m = matcher.name_match(contents)
# major_m = matcher.major_match(contents)
# print(f'\n\nuniv match : {univ_m}\nname match: {name_m}\nmajor match: {major_m}')
# ================================================
end = time.time()
running_time = end - start
print(f'running time : {running_time}')
