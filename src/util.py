import cv2
import os
import sys
from glob import glob


class vid_to_frames:
    
    def __init__(self, data_dir_path, save_dir_path):
        self.data_dir_path = data_dir_path
        self.save_dir_path = save_dir_path
        
    def save_all_frames(self):
        files = glob('self.data_dir_path')
        for file_name in files:
            video_path = os.path.join(self.data_dir_path, file_name)
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print('Video is opening. Please close it')
                return
            
            datasubdir = os.path.basename(self.data_dir_path)
            save_video_path = os.path.join(self.save_dir_path, datasubdir)
            os.makedirs(save_video_path, exist_ok=True)
        
            digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

            n = 0

            while True:
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite('{}_{}.{}'.format(save_video_path, str(n).zfill(digit), 'jpg'), frame)
                    n += 1
                else:
                    return
    
    def video_2_frames(VIDEOS_DIR, TARGET_IMAGES_DIR):　#VIDEOS_DIR内の全体の.mp4ファイルに対して処理を行う
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


    

class operating_files:

    def __init__(self, ):


    def process(self, ):
        #処理内容

    def recursive_file_check(path): #ファイル探索
        # directoryだったら中のファイルに対して再帰的にこの関数を実行
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:#ディレクトリの中にディレクトリ以外のものがあればbreakでディレクトリ内全体に対しての処理の関数を用いることができる
                print(file)
                recursive_file_check(path+'/'+file)
        # fileだったら処理を行う→処理内容が各ファイル1つに対して実行するものであればこれを用いる
        else:
            path = os.path.dirname(path)
            process(path)
