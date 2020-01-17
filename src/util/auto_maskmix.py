import cv2
import numpy as np
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import argparse

def auto_maskmix(FG_IMG, BG_IMG, SPEC_BG_IMG):
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
    print(int(x-foreground_.size[0]/2), int(y-foreground_.size[1]/2))
    print(rate)
    print(foreground_.size[1]/2)
    return back_im

def foreground_random_sampling(BG_IMG, SPEC_BG_IMG):
    background = cv2.imread(BG_IMG)
    # 前景配置位置を指定するアノテーション済み画像
    spec_range = cv2.imread(SPEC_BG_IMG)
    background = cv2.resize(background, (256,256))
    spec_range = cv2.resize(spec_range, (256,256))
    # 前景配置位置の座標をランダムサンプリング
    lower = np.array([0,230,0],dtype=np.uint8)
    upper = np.array([180,255,255],dtype=np.uint8)
    spec_mask = cv2.inRange(spec_range, lower, upper)
    spec_bg = cv2.bitwise_and(background,background,mask=spec_mask)
    #　灰色は[160,160,160]
    spec = np.where(spec_bg<10, 0, 100)[:,:,1]
    index = np.random.choice(np.where(spec.reshape(-1,)>99)[0])
    coord = [int(index/spec.shape[1]), index%spec.shape[1]]
    x,y = coord
    print(spec[x][y])
    return x,y

def mask_with_grabcut(FG_IMG):
    bgr = cv2.imread(FG_IMG)
    bgr = cv2.cvtColor(bgr, cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    mask = np.zeros((h,w), dtype = np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect=(1,1,w,h)
    cv2.grabCut(bgr, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    bgr2 = bgr*mask2[:,:,np.newaxis]
    bgr2 = cv2.resize(bgr2, (256,256))
    #grayscaleに変換する
    gray = cv2.cvtColor(bgr2, cv2.COLOR_BGR2GRAY)
    # 2値化する。
    _, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    # 輪郭抽出する。
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 検出された輪郭内部を255で塗りつぶす。
    mask = np.zeros_like(binary)
    cv2.drawContours(mask, contours, -1, color=(255,255,255), thickness=-1)

    # 以上の手順で前景画像のうち、合成する画素を255としたマスク画像が作成できた。
    mask = cv2.resize(mask, (256,256))
    return mask

def cv2pil(image_cv): # cv2->pillow
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_cv)
    image_pil = image_pil.convert('RGB')

    return image_pil


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for cutmix")

    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("FG_IMG", help="foreground image path")
    parser.add_argument("BG_IMG", help="background image path")
    parser.add_argument("SPEC_BG_IMG", help="background anotated image")

    args = parser.parse_args()

    new_im = auto_maskmix(args.FG_IMG, args.BG_IMG, args.SPEC_BG_IMG)
    new_im.save(args.save_dir,quality=95)