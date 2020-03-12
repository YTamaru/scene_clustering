import tkinter as tk
import os
from time import sleep
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import imutils
import time
import dlib
import cv2
import numpy as np
from PIL import Image, ImageTk
from collections import deque
import argparse
import glob
import auto_maskmix_util

class augmentationtool_Window:
    def __init__(self, main, csv_path):
        self.canvas = Canvas(main, width=1440, height=900)
        self.canvas.grid(row=0,column=0,columnspan=2,rowspan=4)

        #エラーフラグ
        self.error_flag = False
        #画像を取り込む
        #recursive files
        #csvを作成して読み込む
        df = pd.read_csv(csv_file, name=["","",""])
        num_df = len(df)
        #未完成


        #canvas上で左クリックされたときにイベント発生
        self.canvas.bind("<Button-1>", self.canvas_left_click_imsave)
        self.canvas.create_rectangle(10,20,100,50,fill="red")
        self.canvas.pack()

        #画像をcsvから取り込む
        self.my_images = []
        self.file_num = 0
        
        for 

        #最初の画像をセット
        self.image_on_canvas = self.canvas.create_image(
                                        0,
                                        0,
                                        anchor = NW,
                                        image = self.,
                                        )
        #各種ボタンの作成
        #次の画像を表示するボタン
        self.button_next = Button(
                                main,
                                next,
                                text = "Next",
                                command = self.onNextButton,
                                width = 20,
                                height = 5
                                )
        self.button_next.grid(row=2,
                            column=4,
                            columnspan=2,
                            rowspan=2
                            )
        #前の画像を表示するボタン
        self.button_back = Button(main, 
                                back, 
                                text = "Back", 
                                command = self.onBackButton,
                                width = 20,
                                height = 5
                                )
        self.button_back.grid(row=4, 
                            column=4,
                            columnspan=2
                            )
        #選択領域を保存するボタン
        self.button_save = Button(main,
                                text="Save",
                                command=self.onSaveButton,
                                width=25,
                                height = 5
                                )
        self.button_save.grid(row=2,
                            column=6,
                            columnspan=3,
                            rowspan=2
                            )
        
        #メッセージを表示するEntry
        self.message_path = Entry(width=50)
        self.message_path.insert(END,
                                ("This image is "+file)
                                )
        self.message_path.grid(row=6,
                            column=4,
                            columnspan=5
                            )
        
        #エラーメッセージを表示するエントリ
        self.message_error = Entry(width=50)
        if self.error_flag:
            self.message_error.insert(END, ("Please choose the image"))
        else:
            self.message_error.insert(END,())
        self.message.grid(row=7,column=4,columnspan=5)
        
    #------------------------------
    """
    画像上のクリックした座標を取得し，合成画像を保存
    """

    def canvas_left_click_imsave(self, event): #event.x, event.y -> widget左上端からのマウスポインタの位置
        # 貼り付ける画像を選択していなかったらエラーメッセージ
        if :
            self.error_flag = True
        else:
            self.error_flag = False
            print("the coords in the background", (event.x, event.y))
            #ウィジェットに表示する画像は(255,255)
            back_im = auto_maskmix()
            cv2.imwrite(,back_im)
            

    

if __name__ == "__main__":
    root = tk.Tk()
    augmentationtool_Window(root)
    root.mainloop()
    
    
