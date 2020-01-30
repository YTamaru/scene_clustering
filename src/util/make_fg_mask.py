import cv2
import numpy as np
from PIL import Image
import argparse
import pandas as pd

def make_fg_mask(mix_img_csv, save_dir):
    mix_img_ = pd.read_csv(mix_img_csv, names=["path", "data", "mix_img"])
    mix_img_.drop(["data", "mix_img"], axis=1)

    mix_img_np = np.array(mix_img_)
    for row in mix_img_np: 
        print(row[0])
        print(row[0].split("/")[-1])
        img = cv2.imread(row[0])
        mask = np.zeros(img.shape[:2],np.uint8)

        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)

        rect = (0,0,256,256)
        cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]

        img=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        cv2.imwrite(save_dir+row[0].split("/")[-1],mask)