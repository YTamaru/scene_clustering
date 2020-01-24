import numpy as np
import cv2
import argparse
from PIL import Image

def grabcut(IMG):
    bgr = cv2.imread(IMG)
    h, w = bgr.shape[:2]
    mask = np.zeros((h,w), dtype = np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect=(1,1,w,h)
    cv2.grabCut(bgr, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    bgr2 = bgr*mask2[:,:,np.newaxis]
    return bgr2

def cv2pil(image_cv):
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image_cv)
    image_pil = image_pil.convert('RGB')

    return image_pil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for grabcut")

    parser.add_argument("save", help="save as")
    parser.add_argument("IMG", help="image path")


    args = parser.parse_args()
    
    frame = grabcut(args.IMG)
    frame_pil = cv2pil(frame)
    frame_pil.save(args.save)

    # python grabcut.py "/home/tamaru/scene_categorize/main/data/mask/boy.png" "/home/tamaru/scene_categorize/main/data/mix_img/boy.jpg"
