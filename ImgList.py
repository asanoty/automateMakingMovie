import glob
import cv2
import numpy as np
from PIL import Image


class ImgList():
    def __init__(self):
        self.path = "imgs"

    def getImgList(self):
        fileNameListNoProcess = glob.glob("./" + self.path + "/*")
        # 拡張子がpngもしくはjpgではなないものは除外
        fileNameList = []
        for fileName in fileNameListNoProcess:
            if "png" in fileName:
                fileNameList.append(fileName)
            if "jpg" in fileName:
                fileNameList.append(fileName)
        self.fileNameList = fileNameList

    def getImgNum(self):
        return len(self.fileNameList)

    def getImg(self, num):
        # num番目のがファイル名
        fileName = self.fileNameList[num]
        fileName = fileName[2:]
        # 画像を取得
        pil_img = Image.open(fileName)
        img = np.array(pil_img)
        if img.ndim == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        height = img.shape[0]
        width = img.shape[1]
        # 画像のサイズの調整
        baseWidth = 200
        resizedHeight = int(baseWidth/width * height)
        img = cv2.resize(img, (baseWidth, resizedHeight))
        # 画像に移ってる物体の名前を取得
        idx = fileName.find("_")
        materialName = fileName[idx + 1:-4]
        return img, materialName
