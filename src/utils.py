import os

def get_file_list(path):
    """
    디렉토리 내의 모든 파일 경로 가져오기
    """
    files = []
    for root, dirname, filename in os.walk(path):
        for file in filename:
            if file:
                files.append(os.path.join(root, file))

    return files
