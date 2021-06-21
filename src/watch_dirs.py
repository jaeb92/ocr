from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from get_information_standalone import get_context_from_out
import os
import datetime
import time

class IamWatching:
    # watchDir = os.getcwd()
    watchDir = r'../out/ocr_result/graduation/'

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
            while True:
                time.sleep(1)
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
        print(f"파일이 이동되었습니다. : {target}")

    def on_created(self, event): #파일, 디렉터리가 생성되면 실행
        target = event.src_path
        print(f"파일이 생성되었습니다. : {target}")
        get_context_from_out(target)

    # def on_deleted(self, event): #파일, 디렉터리가 삭제되면 실행
    #     print(event)

    # def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
    #     target = event.src_path
    #     print(f"파일이 수정되었습니다. : {target}")
    #     get_context_from_out(target)

# if __name__ == '__main__': #본 파일에서 실행될 때만 실행되도록 함
w = IamWatching()
w.run()