import os
import csv
import time
from glob import glob

num = 1
date_format = '%Y/%m/%d %H:%M:%S'

def maketimestamp(file_path, vid):
    #fileだったときの処理を記述

    is_file = os.path.isfile(file_path)
    print(file_path)
    time_crt = time.strftime(date_format, time.localtime(os.path.getctime(file_path)))
    s_group = os.path.basename(os.path.dirname(file_path))
    l_group = s_group.split('_')[0]
    if is_file:
        vid.append([file_path, l_group, s_group, time_crt])

def writecsv(csv_file, vid):
    with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        for r in vid:
            csv_writer.writerow(r)

def recursive_file_check(path, video_frames, csv_file):
     # directoryだったら中のファイルに対して再帰的にこの関数を実行
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            recursive_file_check(path+'/'+file, video_frames, csv_file)
    # fileだったら1を返す
    else:
        maketimestamp(path, video_frames)
    
    writecsv(csv_file, video_frames)


if __name__ == '__main__':
    path = '../data/insta_mp4'
    csv_file = '../data/vid_crttime.csv'
    video_frames = []
    recursive_file_check(path, video_frames, csv_file)
