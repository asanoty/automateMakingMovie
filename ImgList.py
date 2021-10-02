from ShiritoriElementsList import ShiritoriElementsList
import cv2
import random
import pykakasi
from PIL import Image
import numpy as np


class ImgList():
    def __init__(self):
        backgroundImgPath = "background.jpg"
        self.backgroundImg = cv2.imread(backgroundImgPath)
        self.width = self.backgroundImg.shape[1]
        self.height = self.backgroundImg.shape[0]

    def getSize(self):
        return self.width, self.height

    def makeImgList(self):
        # しりとり要素リストのオブジェクト生成
        shiritoriElementList = ShiritoriElementsList()

        # 空のimgListの生成
        imgList = []

        # 1枚目の画像の追加
        imgList.append(self.backgroundImg)

        # 2枚目以降の画像の追加
        img = self.backgroundImg  # 2枚目以降の画像の土台となる画像
        shiritoriElementList.getImgList()  # しりとり要素リストの生成
        imgMaterialNum = shiritoriElementList.getImgNum()  # しりとり要素数の取得
        for imgMaterialI in range(imgMaterialNum):
            # しりとり要素の画像呼び出し
            materialImg, materialName = shiritoriElementList.getImg(
                imgMaterialI)
            print(materialName)
            # 背景にしりとり画像を重ねる
            img = self.__appendImg(img, materialImg)
            # 文字をかさねる
            imgWithText = img
            imgWithText = self.__drawText(img=img, texts=materialName)
            # リストに追加
            imgList.append(imgWithText)
        return imgList

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
        # cv2->pillow
        pllowMaterialImaga = Image.fromarray(cv2.cvtColor(materialImg, cv2.COLOR_BGR2RGB))
        pllowImg = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # かさね合わせ
        imgLeftX = int(random.randrange(0, self.width - pllowMaterialImaga.size[1]))
        imgTopY = int(random.randrange(0, self.height - pllowMaterialImaga.size[0]))
        pllowImg.paste(pllowMaterialImaga, (imgLeftX, imgTopY))

        # pillow->cv2
        pllowImgPre = np.array(pllowImg, dtype=np.uint8)
        img = cv2.cvtColor(pllowImgPre, cv2.COLOR_RGB2BGR)

        # # 素材の大きさ
        # materialW = materialImg.shape[0]
        # materialH = materialImg.shape[1]
        # # 素材のおかれる範囲
        # randomX = random.randrange(0, self.width - materialW)
        # randomY = random.randrange(0, self.height - materialH)
        # imgLeftX = int(randomX)
        # imgTopY = int(randomY)
        # imgRightX = imgLeftX + materialW
        # imgBottomY = imgTopY + materialH
        # # かさね合わせ
        # print(imgLeftX, imgRightX)
        # print(img.shape, materialImg.shape)
        # img[imgLeftX:imgLeftX+materialW, imgTopY:imgBottomY, :] = materialImg
        return img