import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from get_information_standalone import get_context_from_out
import os
from utils import save_json
import datetime
import time

class IamWatching:
    # watchDir = os.getcwd()
    # 감시할 폴더 경로
    watchDir = r'../out/ocr_result/jol/'

    #watchDir에 감시하려는 디렉토리를 명시한다.
    print(f"Monitoring start {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ... ")
    print(f"Monitoring Directory is {watchDir}")
    def __init__(self):
        self.observer = Observer()   #observer객체를 만듦

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, recursive=True)
        self.observer.start()
        try:
            # 무한루프를 돌면서 폴더 변경을 감지
            while True:
                time.sleep(0.5)
        except:
            self.observer.stop()
            print("Error")
            self.observer.join()

class Handler(FileSystemEventHandler):
    """
    FileSystemEventHandler 클래스를 상속받음.
    on_moved, on_created, on_modified, on_delete 메소드를
    오버라이드하여  파일, 디렉터리가 move, create, update, delete 되면
    특정 로직을 수행
    """

    def on_moved(self, event):
        target = event.src_path
        # src 경로에 파일이 이동된 경우
        print(f"파일이 이동되었습니다. : {target}")

    def on_created(self, event):
        # 파일, 디렉터리가 생성되면 실행
        try:
            target = event.src_path
            print(f"파일이 생성되었습니다. : {target}")

            # 학교명, 학과명, 이름, 아이디, 날짜를 dictionary형태로 반환받고
            # result.json에 저장
            result_dict = get_context_from_out(target)
            print(f"result_dict: {result_dict}")

            save_path = r'../out/dict_result/result.json'
            id = os.path.splitext(os.path.basename(target))[0]
            save_json(save_path, result_dict, id)

        except Exception as e:
            print(f"ERROR: {e}")
    # def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
    #     print(event)

    def on_update(self, event):
        #
        pass

# if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
w = IamWatching()
w.run()