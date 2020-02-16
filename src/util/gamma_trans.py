import add_local_light_paralell
import cv2
import numpy as np
import random
from scipy.stats import norm
import argparse

def gamma_trans(image, light_position=None, direction=None, max_brightness=255, min_brightness=0,
                       mode="gaussian", linear_decay_rate=None, transparency=None):
    frame = cv2.imread(image)
    height, width, _ = frame.shape
    mask = add_local_light_paralell.generate_parallel_light_mask(mask_size=(width, height),
                                        position=light_position,
                                        direction=direction,
                                        max_brightness=max_brightness,
                                        min_brightness=min_brightness,
                                        mode=mode,
                                        linear_decay_rate=linear_decay_rate)
    print(mask.shape)
    look_up_table = np.zeros((256,256), dtype=np.uint8)
    for i in range(256):
        for j in range(256):
            look_up_table[i][j] = 255* (float(i)/255) ** (1.0/mask[i][j])
    image_gamma = cv2.LUT(image, look_up_table)
    return image_gamma


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for cutmix")
    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("data_dir",help="data directory")
    frame = gamma_trans(args.data_dir+"/lab_desk_3_img_000250.png")
    if frame is not None: 
        cv2.imshow("frame", frame)
        cv2.imwrite(args.save_dir+"/add_light.png",frame)
    else:
        print("False")