from log_config import set_logger
from ocr_standalone import str_from_img
# from get_information_standalone import get_context_from_out
# from watch_test import Watcher
import time

# logging 사용하기 위한 설정
logger = set_logger()
logger.info("start program")
# myWatcher = Watcher(r'D:\dv_21\opencv\out\ocr_result\graduation')
# myWatcher.run()
def do_ocr():
    # 입력소스(img) 경로와 출력 경로를 파라미터로 넘기면
    # 입력소스(img)에 대해 OCR 수행후 결과를 txt파일로 저장
    ############## INPUT PATH ###############
    IN_GRADU_PATH = r'../res/img/graduation/'
    IN_SCORE_PATH = r'../res/img/score/'
    #########################################
    ############### OUTPUT PATH #####################
    OUT_GRADU_PATH = r'../out/ocr_result/graduation/'
    OUT_SCORE_PATH = r'../out/ocr_result/score'
    #################################################
    str_from_img(IN_GRADU_PATH, OUT_GRADU_PATH)
    # get_context_from_out()
do_ocr()





