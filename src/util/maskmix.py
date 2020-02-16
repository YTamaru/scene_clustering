import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import argparse

def cv2pil(image_cv):
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_cv)
    image_pil = image_pil.convert('RGB')

    return image_pil

def maskmix(BG_IMG, FG_IMG):
    FG = cv2.imread(FG_IMG)
    BG = cv2.imread(BG_IMG)
    FG = cv2.resize(FG,(256,256))
    BG = cv2.resize(BG,(256,256))
    #GrabCut
    bgr = cv2.cvtColor(FG, cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    mask = np.zeros((h,w), dtype = np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect=(1,1,w,h)
    cv2.grabCut(bgr, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    bgr2 = bgr*mask2[:,:,np.newaxis]
    bgr2 = cv2.resize(bgr2, (256,256))
    #grayscaleに変換
    gray = cv2.cvtColor(bgr2, cv2.COLOR_BGR2GRAY)
    #２値化
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    # 輪郭抽出する。
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 検出された輪郭内部を255で塗りつぶす。
    mask = np.zeros_like(binary)
    cv2.drawContours(mask, contours, -1, color=(255,255,255), thickness=-1)

    # 以上の手順で前景画像のうち、合成する画素を255としたマスク画像が作成できた。
    mask = cv2.resize(mask, (256,256))

    FG = cv2pil(FG)
    BG = cv2pil(BG)

    mask_pil = cv2pil(mask)
    mask_pil = ImageOps.invert(mask_pil)
    mask_im = mask_pil.resize(FG.size).convert("L")

    back_im = BG.copy()
    #マスク画像の左上がx,yとなるので，取りうる値を(-64,128)でランダム
    x, y = random.randint(-64,128), random.randint(-64,128)
    #画像の縮小を0.5~1.0で行う
    rate = np.random.rand()*0.5 + 0.5
    #画像の回転を360度の範囲でランダムに行う
    rotate = random.randint(0,360)
    foreground_ = FG.resize((int(FG.width*rate), int(FG.height*rate))).rotate(rotate)
    mask_im_ = mask_im.resize((int(mask_im.width*rate), int(mask_im.height*rate))).rotate(rotate)
    back_im.paste(foreground_, (x, y), mask_im_)
    return back_im



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for cutmix")

    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("FG_IMG", help="foreground image path")
    parser.add_argument("BG_IMG", help="background image path")

    args = parser.parse_args()

    new_im = maskmix(args.BG_IMG, args.FG_IMG)
    new_im.save(args.save_dir,quality=95)