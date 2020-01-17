import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
import argparse

def imshow(img):
    if img.ndim == 2:
        plt.imshow(img, cmap="gray")
    else:
        plt.show(img[...,::-1])
    plt.axis("off")
    plt.show()

def maskmix(BG_IMG, FG_IMG):
    background = cv2.imread(BG_IMG)

    foreground = cv2.imread(FG_IMG)
    foreground = cv2.resize(foreground, (256,256))

    # マスク画像作成
    h, w = foreground.shape[:2] #前景画像の大きさ

    mask = np.zeros((h, w), dtype = np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect=(1,1,w,h)
    cv2.grabCut(foreground, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    foreground = foreground*mask2[:,:,np.newaxis]
    gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    #輪郭を抽出
    contours,_ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(binary)
    cv2.drawContours(mask, contours, -1, color=255, thickness=-1)
    imshow(mask)
    cv2.imshow("foreground", foreground)

    #背景画像と前景画像の合成
    x, y = random.randint(0,256), random.randint(0, 256) #背景画像の座標上で前景画像を貼り付ける位置
    roi = background[y:y+h,x:x+w,:]
    result = np.where(np.expand_dims(mask==255,-1), foreground, roi)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for cutmix")

    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("FG_IMG", help="foreground image path")
    parser.add_argument("BG_IMG", help="background image path")

    args = parser.parse_args()

    # FG_IMG = "/home/tamaru/scene_categorize/main/data/dog.jpg"
    # BG_IMG = "/home/tamaru/scene_categorize/main/data/lab_table_4_img_000230.png"
    # save_dir = "/home/tamaru/scene_categorize/main/data"
    cv2.imwrite(args.save_dir, maskmix(args.BG_IMG, args.FG_IMG))