#coding: utf-8
import argparse
import cv2
import os

def argparser():
    """
    実行時に　オプションをつける
    image: 画像のフルパス
    --func: SR: SpectralResidual_create
            FG: FineGrained_create

    顕著性マップ
    SpectralResidual->
    FineGrained->エッジを含める
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=str, help="input image")
    parser.add_argument("--func", type=str, choices=["SR", "FG"], default="SR")
    return parser.parse_args()


def main(dir_path):
    """

    """
    args = argparser()

    img = cv2.imread(args.image)
    if img is None:
        exit()
    filename = os.path.basename(args.image)
    img_name = filename.split(".")[0] + "_salmap" +".png"
    
    saliency = None
    if args.func == "SR":
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    elif args.func == "FG":
        saliency = cv2.saliency.StaticSaliencyFineGrained_create()

    if saliency is None:
        exit()

    (success, saliencyMap) = saliency.computeSaliency(img)
    saliencyMap = (saliencyMap*255).astype("uint8")

    cv2.imwrite(dir_path+img_name,saliencyMap)

if __name__=="__main__":
    dir_path = "../data/insta_salmap"
    main(dir_path)