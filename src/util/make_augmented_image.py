import pandas as pd
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import random
import os
import auto_maskmix_util

def make_augmented_image(train_csv, bg_mask_csv, mix_img_csv, save_dir, cls):
    bg_mask = pd.read_csv(bg_mask_csv)
    mix_img = pd.read_csv(mix_img_csv)
    bg_mask = bg_mask.drop(["data", "mask_cube"], axis=1)
    mix_img = mix_img.drop(["data", "mix_img"], axis=1)

    bg_mask = bg_mask.sort_values("path")
    bg_mask = bg_mask.reset_index(drop=True)
    mix_img = mix_img.sort_values("path")
    mix_img = mix_img.reset_index(drop=True)

    background = pd.read_csv(train_csv, names=["path", "data", "mask_cube"])
    background = background.drop(["data"], axis=1)
    background = background[background.mask_cube==cls]
    background = background.drop(["mask_cube"], axis=1)
    background = background.sort_values("path")
    background = background.reset_index(drop=True)

    auto_maskmix_2all(background, bg_mask, mix_img, save_dir)

class cv2OverlayImage(object):
    """
    [summary]
      Opencv2形式の画像に指定画像を重ねる
    """

    def __init__(self):
        pass

    @classmethod
    def overlay(
            cls,
            cv2_background_image,
            cv2_overlay_image,
            point,
    ):
        """
        [summary]
          Opencv2形式の画像に指定画像を重ねる
        Parameters
        ----------
        cv2_background_image : [Opencv2 Image]
        cv2_overlay_image : [Opencv2 Image]
        point : [(x, y)]
        Returns : [Opencv2 Image]
        """
        overlay_height, overlay_width = cv2_overlay_image.shape[:2]

        # Opencv2形式の画像をPIL形式に変換(α値含む)
        # 背景画像ユーザー
        cv2_rgb_bg_image = cv2.cvtColor(cv2_background_image, cv2.COLOR_BGR2RGB)
        pil_rgb_bg_image = Image.fromarray(cv2_rgb_bg_image)
        pil_rgba_bg_image = pil_rgb_bg_image.convert('RGBA')
        # オーバーレイ画像
        cv2_rgb_ol_image = cv2.cvtColor(cv2_overlay_image, cv2.COLOR_BGRA2RGBA)
        pil_rgb_ol_image = Image.fromarray(cv2_rgb_ol_image)
        pil_rgba_ol_image = pil_rgb_ol_image.convert('RGBA')
        # composite()は同サイズ画像同士が必須のため、合成用画像を用意
        pil_rgba_bg_temp = Image.new('RGBA', pil_rgba_bg_image.size,
                                     (255, 255, 255, 0))
        # 座標を指定し重ね合わせる
        pil_rgba_bg_temp.paste(pil_rgba_ol_image, point, pil_rgba_ol_image)
        result_image = \
            Image.alpha_composite(pil_rgba_bg_image, pil_rgba_bg_temp)

        # Opencv2形式画像へ変換
        cv2_bgr_result_image = cv2.cvtColor(
            np.asarray(result_image), cv2.COLOR_RGBA2BGRA)

        return cv2_bgr_result_image

def auto_maskmix(FG_IMG, BG_IMG, SPEC_BG_IMG):
    foreground = cv2.imread(FG_IMG, cv2.IMREAD_UNCHANGED)
    background = cv2.imread(BG_IMG)
    foreground = cv2.resize(foreground, (256,256))
    background = cv2.resize(background, (256,256))
    
    coord = auto_maskmix_util.foreground_random_sampling(BG_IMG, SPEC_BG_IMG)
    
    back_im = background.copy()
    x, y = coord
    rate = np.random.rand()*0.2 + 0.2
    rotate = random.randint(0,360)
    size = (int(foreground.shape[1]*rate), int(foreground.shape[1]*rate))
    foreground_ = cv2.resize(foreground, size)
    #前景画像の配置位置の座標は前景画像の左上なので，中心に平行移動する->未完成
    point = (int(x-foreground_.shape[1]/2), int(y-foreground_.shape[0]/2))
    back_im = cv2OverlayImage.overlay(background ,foreground_, point)
    print("Foreground center coordinate", int(x-foreground_.shape[0]/2), int(y-foreground_.shape[1]/2))
    print("Foreground Rate:", rate)
    print("Foreground Size", foreground_.shape[1])
    return back_im

def auto_maskmix_2all(background, bg_mask, mix_img, save_dir):
    bg_col_name = background.columns.values
    bg_mask_col_name = bg_mask.columns.values
    mix_col_name = mix_img.columns.values
    background_np = np.array(background)
    bg_mask_np = np.array(bg_mask)
    mix_img_np = np.array(mix_img)
    i = 0
    while(background_np[i][bg_col_name.tolist().index("path")] is not None):
        rand_mix = random.randint(0,len(mix_img_np)-1)
        print("Foreground:", rand_mix)
        back_im = auto_maskmix(mix_img_np[rand_mix][0], background_np[i][bg_col_name.tolist().index("path")], bg_mask_np[i][bg_mask_col_name.tolist().index("path")])
        cv2.imwrite(save_dir+"/"+background_np[i][bg_col_name.tolist().index("path")].split('/')[-1], back_im)
        i += 1
        print("------------")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="for augmented images")

    parser.add_argument("train_csv", help="train csv path")
    parser.add_argument("bg_mask", help="background mask csv path")
    parser.add_argument("mix_img_csv", help="mix_img csv path")
    parser.add_argument("save_dir", help="save directory")
    parser.add_argument("cls", help="data class name")

    args = parser.parse_args()

    make_augmented_image(args.train_csv, args.bg_mask_csv, args.mix_img_csv, args.save_dir, args.cls)