import cv2
import os
import sys
from glob import glob
import shutil
import py360convert
import numpy as np
from PIL import Image


def video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR):
    files = glob(VIDEOS_DIR+'/'+'*.png')
    num = 1

        # Remove and make a directory.
    if os.path.exists(TARGET_IMAGES_DIR):
        shutil.rmtree(TARGET_IMAGES_DIR)  # Delete an entire directory tree
    if not os.path.exists(TARGET_IMAGES_DIR):
        os.makedirs(TARGET_IMAGES_DIR)	# Make a directory

    for file in files:
        e_frame = np.array(Image.open(file))
        cube_frame = py360convert.e2c(e_frame, face_w=256, mode="bilinear", cube_format="list")
        for i in range(6):
            cube_img = Image.fromarray(cube_frame[i])

            if not os.path.exists(TARGET_IMAGES_DIR+'/'+str(i)):
                os.makedirs(TARGET_IMAGES_DIR+'/'+str(i))	# Make a directory
            cube_img.save(TARGET_IMAGES_DIR+'/'+str(i)+'/'+os.path.basename(file))
            print('Save', TARGET_IMAGES_DIR+'/'+str(i)+'/'+os.path.basename(file))
        print('Save '+str(num)+' frame')
        num += 1
    print('Save a diretory')

def recursive_file_check(VIDEOS_DIR, TARGET_IMAGES_DIR, itenum):
     # directoryだったら中のファイルに対して再帰的にこの関数を実行
    if os.path.isdir(VIDEOS_DIR):
        files = os.listdir(VIDEOS_DIR)
        itenum += 1
        for file in files:
            if os.path.isdir(VIDEOS_DIR +'/'+file):
                recursive_file_check(VIDEOS_DIR+'/'+file, TARGET_IMAGES_DIR, itenum)
            else:   #ディレクトリの中にディレクトリ以外のものがあればbreak
                TARGET_IMAGES_DIR_HEAD = ''
                itenum -= 1
                if itenum > 0:
                    for i in range(itenum):    
                        TARGET_IMAGES_DIR_HEAD = os.path.join(TARGET_IMAGES_DIR_HEAD, VIDEOS_DIR.split('/')[-itenum+i])
                TARGET_IMAGES_DIR = os.path.join(TARGET_IMAGES_DIR, TARGET_IMAGES_DIR_HEAD)
                video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR)
                break

    # fileだったら処理を行う→処理内容が各ファイル1つに対して実行するものであればこれを用いる
    # else:
    #     path = os.path.dirname(VIDEOS_DIR)
    #     print(path)
    #     TARGET_IMAGES_DIR = os.path.join(TARGET_IMAGES_DIR, os.path.basename(os.path.dirname(path)), os.path.basename(path)) 
    #     video_2_frames(path, TARGET_IMAGES_DIR)

if __name__ == "__main__":
    data_dir_path = '/home/tamaru/scene_categorize/main/data/insta_frames/professorroom'
    save_dir_path = '/home/tamaru/scene_categorize/main/data/insta_cube/professorroom'
    recursive_file_check(data_dir_path, save_dir_path, 0)