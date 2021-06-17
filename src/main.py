from log_config import set_logger
from ocr_standalone import str_from_img
# logging 사용하기위한 인스턴스 생성
def main():

    IN_GRADU_PATH = r'../res/img/graduation/'
    IN_SCORE_PATH = r'../res/img/score/'

    OUT_GRADU_PATH = r'../out/ocr_result/graduation/'
    OUT_SCORE_PATH = r'../out/ocr_result/score'

    logger = set_logger()
    logger.info("start program")
    
    # 이미지 ocr 수행후 결과를 파일로 저장
    str_from_img(IN_GRADU_PATH, OUT_GRADU_PATH)


    
# ocr 수행

main()

