import os
import shutil

done_path = r'../res/img/'
score_path = os.path.join(done_path, 'png_han_sung')
gradu_path = os.path.join(done_path, 'png_han_jol')
file_list = os.listdir(done_path)
for file in file_list:
    os.mkdir(score_path) if not os.path.exists(score_path) else ''
    os.mkdir(gradu_path) if not os.path.exists(gradu_path) else ''
    target_file = os.path.join(done_path, file)

    if '성' in file:
        shutil.move(target_file, score_path)
    elif '졸' in file:
        shutil.move(target_file, gradu_path)
    else:
        pass
    # print(file)
    # print(os.path.dirname(file))
# print(file_list)