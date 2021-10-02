from ImgList import ImgList
import cv2
import numpy as np
import pykakasi
import random


class MovieMaker():
    def __init__(self):
        # 動画の設定
        backgroundImgPath = "background.jpg"
        self.backgroundImg = cv2.imread(backgroundImgPath)
        self.videoW = self.backgroundImg.shape[1]
        self.videoH = self.backgroundImg.shape[0]

    def makeMovie(self):
        # 動画の設定
        outputFilePath = "movie.mp4"
        CLIP_FPS = 1  # 1秒間に20枚のフレーム
        codec = cv2.VideoWriter_fourcc(*'mp4v')

        # オブジェクトの生成
        video = cv2.VideoWriter(outputFilePath, codec, CLIP_FPS,
                                (self.videoW, self.videoH))  # 動画
        imgList = ImgList()  # 画像のリスト

        # 画像リストの生成
        imgList.getImgList()

        # 動画の背景の生成
        img = self.backgroundImg

        # 動画の作成
        imgMaterialNum = imgList.getImgNum()
        for frameNum in range(imgMaterialNum):
            # 素材となる画像とその名前を取得
            if frameNum >= 1:
                imgMaterialNum = frameNum - 1
                materialImg, materialName = imgList.getImg(imgMaterialNum)
                print(materialName)
                # 画像に素材をのせる
                img = self.__appendImg(img, materialImg)
                # 画像に文字を載せる
                imgWithText = img
                imgWithText = self.__drawText(img=img, texts=materialName)
                # 画像を動画に反映
                video.write(imgWithText)
            else:
                # 画像を動画に反映
                video.write(img)

        # 動画の出力
        video.release()

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

    def __appendImg(self, img, materialImg):
        materialWHalf = int(materialImg.shape[1] / 2)
        materialHHalf = int(materialImg.shape[0] / 2)
        boudaryY = self.videoH / 2 - materialWHalf
        boundayX = self.videoW / 2 - materialWHalf
        imgCenterY = int(self.videoH / 2 +
                         random.randrange(-boudaryY, boudaryY))
        imgCenterX = int(self.videoW / 2 +
                         random.randrange(-boundayX, boundayX))
        img[imgCenterY - materialHHalf:imgCenterY - materialHHalf +
            materialImg.shape[0], imgCenterX - materialWHalf:imgCenterX -
            materialWHalf + materialImg.shape[1]] = materialImg  # 画像
        return img