import cv2
import os
import sys
from glob import glob
import shutil
import time
import csv
import argparse

date_format = '%Y/%m/%d %H:%M:%S'


def maketimestamp(frame_path, vid_path, TARGET_IMAGES_DIR_HEAD, vid_data):
    #fileだったときの処理を記述
    is_file = os.path.isfile(vid_path)
    time_crt = time.strftime(date_format, time.localtime(os.path.getctime(vid_path)))
    l_group = TARGET_IMAGES_DIR_HEAD.split('/')[0]
    if len(TARGET_IMAGES_DIR_HEAD.split('/')) == 1:
        s_group = TARGET_IMAGES_DIR_HEAD.split('/')[0]
    else:
        s_group = TARGET_IMAGES_DIR_HEAD.split('/')[1]

    if is_file:
        vid_data.append([frame_path, l_group, s_group, time_crt])

def video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR, TARGET_IMAGES_DIR_HEAD, vid_data):
    files = glob(VIDEOS_DIR+'/'+'*.mp4')
    image_file_temp='img_%s.png'
    num = 0

        # Remove and make a directory.
    if os.path.exists(TARGET_IMAGES_DIR):
        shutil.rmtree(TARGET_IMAGES_DIR)  # Delete an entire directory tree
    if not os.path.exists(TARGET_IMAGES_DIR):
        os.makedirs(TARGET_IMAGES_DIR)	# Make a directory

    for file in files:
        cap = cv2.VideoCapture(file)
        fps = round(cap.get(cv2.CAP_PROP_FPS))

        i = 0
        while(cap.isOpened()):
            flag, frame = cap.read()  # Capture frame-by-frame
            if flag == False:
                break  # A frame is not left
            # if(i%(fps/3)==0):
            if(i%1==-0):
                cv2.imwrite(TARGET_IMAGES_DIR+'/'+os.path.basename(TARGET_IMAGES_DIR)+'_'+str(num)+'_'+image_file_temp % str(i).zfill(6), frame)  # Save a frame
                print('Save', TARGET_IMAGES_DIR+'/'+os.path.basename(TARGET_IMAGES_DIR)+'_'+str(num)+'_'+image_file_temp % str(i).zfill(6))
                frame_path = TARGET_IMAGES_DIR+'/'+os.path.basename(TARGET_IMAGES_DIR)+'_'+str(num)+'_'+image_file_temp % str(i).zfill(6)
                maketimestamp(frame_path,file, TARGET_IMAGES_DIR_HEAD, vid_data)
                i += 1
            else:
                i += 1
        cap.release()  # When everything done, release the capture
        num += 1
        print('Save '+str(num)+' vid')
    print('Save a diretory')

def recursive_file_check(VIDEOS_DIR, TARGET_IMAGES_DIR, itenum, vid_data):
     # directoryだったら中のファイルに対して再帰的にこの関数を実行
    if os.path.isdir(VIDEOS_DIR):
        files = os.listdir(VIDEOS_DIR)
        itenum += 1
        for file in files:
            if os.path.isdir(VIDEOS_DIR +'/'+file):
                recursive_file_check(VIDEOS_DIR+'/'+file, TARGET_IMAGES_DIR, itenum, vid_data)
            else:   #ディレクトリの中にディレクトリ以外のものがあればbreak
                TARGET_IMAGES_DIR_HEAD = ''
                itenum -= 1
                if itenum > 0:
                    for i in range(itenum):    
                        TARGET_IMAGES_DIR_HEAD = os.path.join(TARGET_IMAGES_DIR_HEAD, VIDEOS_DIR.split('/')[-itenum+i])
                TARGET_IMAGES_DIR = os.path.join(TARGET_IMAGES_DIR, TARGET_IMAGES_DIR_HEAD)
                video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR, TARGET_IMAGES_DIR_HEAD, vid_data)
                break
    # fileだったら処理を行う→処理内容が各ファイル1つに対して実行するものであればこれを用いる
    # else:
    #     path = os.path.dirname(VIDEOS_DIR)
    #     print(path)
    #     TARGET_IMAGES_DIR = os.path.join(TARGET_IMAGES_DIR, os.path.basename(os.path.dirname(path)), os.path.basename(path)) 
    #     video_2_frames(path, TARGET_IMAGES_DIR)

def writecsv(csv_file, vid_data):
    with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        for r in vid_data:
            csv_writer.writerow(r)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="for cutmix")
    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("data_dir",help="data directory")
    parser.add_argument("csv_file",help="csv_file")

    vid_data = []
    recursive_file_check(args. data_dir, args.save_dir, 0, vid_data)
    writecsv(args.csv_file, vid_data)