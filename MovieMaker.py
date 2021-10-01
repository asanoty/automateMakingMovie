from ImgList import ImgList
import cv2
import numpy as np
import pykakasi


class MovieMaker():
    def __init__(self):
        # 動画の設定
        self.W = 640
        self.H = 480
        CLIP_FPS = 1  # 1秒間に20枚のフレーム
        filePath = "movie.mp4"
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        # 動画のオブジェクト
        self.video = cv2.VideoWriter(filePath, codec, CLIP_FPS,
                                     (self.W, self.H))

    def makeMovie(self):
        # オブジェクトの生成
        imgList = ImgList()

        # 画像リストの生成
        imgList.getImgList()

        # 動画の作成
        imgNum = imgList.getImgNum()
        for num in range(imgNum):
            # 動画に反映する画像の生成
            img = self.__getBackGroundImg()
            # 背景に画像と文字をつける
            materialImg, materialName = imgList.getImg(num=num)
            print(materialName)
            imgCenterY = int(self.H / 2)
            imgCenterX = int(self.W / 2)
            materialWHalf = int(materialImg.shape[1] / 2)
            materialHHalf = int(materialImg.shape[0] / 2)
            img[imgCenterY - materialHHalf:imgCenterY - materialHHalf +
                materialImg.shape[0], imgCenterX - materialWHalf:imgCenterX -
                materialWHalf + materialImg.shape[1]] = materialImg  # 画像
            imgWithText = self.__drawText(img=img, texts=materialName)
            # 画像を動画に反映
            self.video.write(imgWithText)

        # 動画の出力
        self.video.release()

    def __getBackGroundImg(self):
        BG_COLOR = (79, 62, 70)
        img = np.zeros((self.H, self.W, 3), np.uint8)
        img = cv2.rectangle(img, (0, 0), (self.W - 1, self.H - 1), BG_COLOR,
                            -1)
        return img

    def __drawText(self, img, texts, w_ratio=0.35, h_ratio=0.15, alpha=0.4):
        def draw_texts(img, texts, font_scale=0.7, thickness=2):
            h, w, c = img.shape
            offset_x = 10  # 左下の座標
            initial_y = 0
            dy = int(img.shape[1] / 15)
            color = (0, 0, 0)  # black

            texts = [texts] if type(texts) == str else texts

            for i, text in enumerate(texts):
                offset_y = initial_y + (i + 1) * dy
                cv2.putText(img, text, (offset_x, offset_y),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, color,
                            thickness, cv2.LINE_AA)

        # ひらがなをローマ字に変換
        kakasi = pykakasi.kakasi()
        kakasi.setMode('H', 'a')
        conversion = kakasi.getConverter()
        texts = conversion.do(texts)

        # 文字をのせるためのマットを作成する
        overlay = img.copy()
        pt1 = (0, 0)
        pt2 = (int(img.shape[1] * w_ratio), int(img.shape[0] * h_ratio))

        mat_color = (200, 200, 200)
        fill = -1  # -1にすると塗りつぶし
        cv2.rectangle(overlay, pt1, pt2, mat_color, fill)

        mat_img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        draw_texts(mat_img, texts)

        return mat_img