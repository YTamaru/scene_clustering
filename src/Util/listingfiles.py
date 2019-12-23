import os
import csv
import time
from glob import glob

def makelist(file_path, video_frames):
    #fileだったときの処理を記述

    is_file = os.path.isfile(file_path)

    s_group = os.path.basename(os.path.dirname(file_path))
    l_group = s_group.split('_')[0]
    if is_file:
        video_frames.append([file_path, l_group, s_group])

def writecsv(csv_file, video_frames):
    with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        for r in video_frames:
            csv_writer.writerow(r)

def recursive_file_check(path, video_frames, csv_file):
     # directoryだったら中のファイルに対して再帰的にこの関数を実行
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            print(file)
            recursive_file_check(path+'/'+file, video_frames, csv_file)
    # fileだったら1を返す
    else:
        makelist(path, video_frames)
    
    writecsv(csv_file, video_frames)


if __name__ == '__main__':
    path = '../data/insta_frames'
    csv_file = '../data/video_frames.csv'
    video_frames = []
    recursive_file_check(path, video_frames, csv_file)

