import cv2
import numpy as np
import pandas as pd
import argparse
import os
import re


class mouseParam:
    def __init__(self, input_img_name):
        #マウス入力用のパラメータ
        self.mouseEvent = {"x":None, "y":None, "event":None, "flags":None}
        #マウス入力の設定
        cv2.setMouseCallback(input_img_name, self.__CallBackFunc, None)
    
    #コールバック関数
    def __CallBackFunc(self, eventType, x, y, flags, userdata):
        
        self.mouseEvent["x"] = x
        self.mouseEvent["y"] = y
        self.mouseEvent["event"] = eventType    
        self.mouseEvent["flags"] = flags    

    #マウス入力用のパラメータを返すための関数
    def getData(self):
        return self.mouseEvent
    
    #マウスイベントを返す関数
    def getEvent(self):
        return self.mouseEvent["event"]                

    #マウスフラグを返す関数
    def getFlags(self):
        return self.mouseEvent["flags"]                

    #xの座標を返す関数
    def getX(self):
        return self.mouseEvent["x"]  

    #yの座標を返す関数
    def getY(self):
        return self.mouseEvent["y"]  

    #xとyの座標を返す関数
    def getPos(self):
        return (self.mouseEvent["x"], self.mouseEvent["y"])

    
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


        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="for augmentationtool")
    #オーグメンテーションを行う画像のcsv
    parser.add_argument("csv_path", help="images csv path")
    
    args = parser.parse_args()

    df = pd.read_csv(args.csv_path, names=["path", "s_class", "class"])
    df = df.drop(["s_class"], axis=1)
    df = df.sort_values("path")
    df = df.reset_index(drop=True)
    
    df_col_name = df.columns.values()
    df_np = np.array(df)
    i = 0

    #貼り付ける画像のdict
    fg_dict = {
        "1":,
        "2":,
        "3":,
        "4":

    }

    #画像を一枚ずつ読み出して実行
    while(df_np[i][df_col_name.tolist().index("path")] is not None):
        i += 1
        bg = cv2.imread(df_np[i][df_col_name.tolist().index("path")])
        #パラメータの設定
        rate = np.random.rand()*0.2+0.2
        #貼り付ける画像を番号で指定
        print(fg_dict)
        print("select the foreground image:")
        dict_num = str(input())
        fg = cv2.imread(fg_dict.get(dict_num))

        size = (int(fg.shape[0]*rate), int(fg.shape[1]*rate))
        fg_ = cv2.resize(fg, size)
        #画像の表示
        cv2.imshow("input window", bg)
    
        #コールバックの設定
        mouseData = mouseParam("input window")
        save_dir = "../data/"+df_np[i][df_col_name.tolist().index("class")]
    
        while True:
            cv2.waitKey(20)
            #左クリックがあったら表示
            if mouseData.getEvent() == cv2.EVENT_LBUTTONDOWN:
                back_im = cv2OverlayImage.overlay(bg, fg_, mouseData.getMouse())
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)	# Make a directory
                cv2.imwrite(save_dir+"/"+re.split("/", df_np[i][df_col_name.tolist().index("path")])[-1],back_im)

            #右クリックがあったら終了
            elif mouseData.getEvent() == cv2.EVENT_RBUTTONDOWN:
                break　　
                
        cv2.destroyAllWindows()            
        print("Finished a image")
    print("Finished all")