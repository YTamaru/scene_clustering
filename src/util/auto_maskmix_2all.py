import auto_maskmix
import cv2
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import argparse


def recursive_file_check(DATA_DIR, TARGET_DIR, itenum):
     # directoryだったら中のファイルに対して再帰的にこの関数を実行
    if os.path.isdir(DATA_DIR):
        files = os.listdir(DATA_DIR)
        itenum += 1
        for file in files:
            if os.path.isdir(DATA_DIR +'/'+file):
                recursive_file_check(DATA_DIR+'/'+file, TARGET_DIR, itenum)
            else:   #ディレクトリの中にディレクトリ以外のものがあればbreak
                TARGET_DIR_HEAD = ''
                itenum -= 1
                if itenum > 0:
                    for i in range(itenum):    
                        TARGET_DIR_HEAD = os.path.join(TARGET_DIR_HEAD, DATA_DIR.split('/')[-itenum+i])
                TARGET_DIR = os.path.join(TARGET_DIR, TARGET_DIR_HEAD)
                auto_maskmix_2all(DATA_DIR, TARGET_DIR)
                break

def auto_maskmix_2all(FG_IMG, BG_IMG, SPEC_BG_IMG):
    foreground = Image.open(FG_IMG)
    background = Image.open(BG_IMG)
    foreground = foreground.resize((256,256))
    background = background.resize((256,256))

    mask = mask_with_grabcut(FG_IMG)
    coord = foreground_random_sampling(BG_IMG, SPEC_BG_IMG)

    mask_pil = cv2pil(mask)
    mask_pil = ImageOps.invert(mask_pil)
    mask_im = mask_pil.resize(foreground.size).convert("L")

    back_im = background.copy()
    x, y = coord
    rate = np.random.rand()*0.5 + 0.5
    rotate = random.randint(0,360)
    foreground_ = foreground.resize((int(foreground.width*rate), int(foreground.height*rate))).rotate(rotate)
    mask_im_ = mask_im.resize((int(mask_im.width*rate), int(mask_im.height*rate))).rotate(rotate)
    #前景画像の配置位置の座標は前景画像の左上なので，中心に平行移動する->未完成
    back_im.paste(foreground_, (int(x-foreground_.size[0]/2), int(y-foreground_.size[1]/2)), mask_im_)
    print("Foreground center coordinate", int(x-foreground_.size[0]/2), int(y-foreground_.size[1]/2))
    print("Foreground Rate:", rate)
    print("Foreground Size", foreground_.size[1])
    return back_im

