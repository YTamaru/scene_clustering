import cv2
import os
import sys
from glob import glob
import shutil

# 動画のすべてのフレームを画像ファイルとして保存
def save_all_frames(data_dir_path, save_dir_path, i):
    files = glob('data_dir_path')
    datasubdir = ''
    if i > 0:
        for j in range(i-1):    
            datasubdir = os.path.join(datasubdir, data_dir_path.split('/')[-j-1])
    save_dir_path = os.path.join(save_dir_path, datasubdir)
    save_video_path = os.path.join(save_dir_path, datasubdir)
    os.makedirs(save_video_path, exist_ok=True)
    for file_name in files:
        video_path = os.path.join(data_dir_path, file_name)
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print('Error')
            return


        digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

        n = 0

        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('{}_{}.{}'.format(save_video_path, str(n).zfill(digit), 'jpg'), frame)
                n += 1
            else:
                return


def video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR):
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
                # 1秒毎にフレームを抽出
            if(i%fps==0):
                cv2.imwrite(TARGET_IMAGES_DIR+'/'+os.path.basename(TARGET_IMAGES_DIR)+'_'+str(num)+'_'+image_file_temp % str(i).zfill(6), frame)  # Save a frame
                i += 1
                print('Save', TARGET_IMAGES_DIR+'/'+os.path.basename(TARGET_IMAGES_DIR)+'_'+str(num)+'_'+image_file_temp % str(i).zfill(6))
            else:
                i += 1
        cap.release()  # When everything done, release the capture
        num += 1
        print('Save '+str(num)+' vid')
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
    data_dir_path = '../data/insta_mp4'
    save_dir_path = '../data/insta_frames'
    recursive_file_check(data_dir_path, save_dir_path, 0)