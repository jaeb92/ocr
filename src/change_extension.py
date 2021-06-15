import glob
import os.path
path = '../testdir'
files = glob.glob(path + "/*")
flag = input('확장자를 변경하시겠습니까?(y/n) >> ')
ext = input("어떤 확장자로 변경하시겟습니까 ex) jpg, json, txt >>")
if flag == 'y' or flag == 'Y':
    for x in files:
        if not os.path.isdir(x):
            filename = os.path.splitext(x)
            # tmp = filename[0].replace('.pdf', '')
            try:
                os.rename(x, filename[0], '')
                # os.rename(x, tmp + '.jpg')
            except:
                pass
    print('변경완료')

elif flag == 'n' or flag == 'N':
    exit()