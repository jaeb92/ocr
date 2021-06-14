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

def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

#
# matcher = Matcher([
#     'name',
#     'university',
#     'major',
# ])

# print(matcher.match(["동국대학교 컴퓨터공학과 황재빈"]))
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

# break the input languages into a comma separated list
# langs = args["langs"].split(",")
# print("[INFO] OCR'ing with the following languages: {}".format(langs))
# load the input image from disk

ff = np.fromfile(args["image"], np.uint8)
image = cv2.imdecode(ff, cv2.IMREAD_UNCHANGED)
image = cv2.resize(image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
# image = cv2.imread(args["image"])

# print(type(image))
# print(image)
# OCR the input image using EasyOCR
print("[INFO] OCR'ing input image...")
reader = Reader(['ko', 'en'], gpu=args["gpu"] > 0, recognizer='Transformer')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
results = reader.readtext(gray)
# print(results)
# print(f'resutls: {results}')
contents = []
for word in results:
    contents.append(word[1].replace('\t', '').replace(' ', '').replace(':', ' '))
    # print(results[i][1].replace('\t', '').replace(' ', ''), end=' ')
# print(' '.join(contents))

# print('contents:', contents)
matcher.match(contents)
# ================================================
# univ_m = matcher.university_match(contents)
# name_m = matcher.name_match(contents)
# major_m = matcher.major_match(contents)
# print(f'\n\nuniv match : {univ_m}\nname match: {name_m}\nmajor match: {major_m}')
# ================================================

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
