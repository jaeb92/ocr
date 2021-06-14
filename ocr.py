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
from ocr_matcher import Matcher

def cleanup_text(text):
	# strip out non-ASCII text so we can draw the text on the image
	# using OpenCV
	return "".join([c if ord(c) < 128 else "" for c in text]).strip()

matcher = Matcher()

start = time.time()
ap = argparse.ArgumentParser()

ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-l", "--langs", type=str, default="en",
	help="comma separated list of languages to OCR")
ap.add_argument("-g", "--gpu", type=int, default=-1,
	help="whether or not GPU should be used")
args = vars(ap.parse_args())

# break the input languages into a comma separated list
langs = args["langs"].split(",")
print("[INFO] OCR'ing with the following languages: {}".format(langs))
# load the input image from disk

ff = np.fromfile(args["image"], np.uint8)
image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
# image = cv2.imread(args["image"])

# print(type(image))
# print(image)
# OCR the input image using EasyOCR
print("[INFO] OCR'ing input image...")
reader = Reader(langs, gpu=args["gpu"] > 0)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

results = reader.readtext(gray)

# print(results)
# print(f'resutls: {results}')
# for i in range(len(results)):
#     print(results[i][1].replace('\t', '').replace(' ', ''), end='\t')

# loop over the results
for (bbox, text, prob) in results:
    text = text.replace(' ', '')
	# display the OCR'd text and associated probability
    if matcher.university_match(text):
        print("[INFO] {:.4f}: {}".format(prob, text.replace(' ', '')))

        # # unpack the bounding box
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
# image = cv2.resize(image, None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)
# cv2.imshow("Image", image)
# cv2.waitKey(0)
