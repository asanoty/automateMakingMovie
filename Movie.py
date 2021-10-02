from ShiritoriElementsList import ShiritoriElementsList
from ImgList import ImgList
import cv2
import numpy as np
import pykakasi
import random


class Movie():
    def __init__(self):
        pass

    def makeMovie(self):
        # 画像のリスト生成
        imgListObject = ImgList()
        imgList = imgListObject.makeImgList()

        # 動画の設定
        outputFilePath = "movie.mp4"
        CLIP_FPS = 1  # 1秒間に20枚のフレーム
        codec = cv2.VideoWriter_fourcc(*'mp4v')
        videoW, videoH = imgListObject.getSize()
        # 動画オブジェクトの作成
        video = cv2.VideoWriter(outputFilePath, codec, CLIP_FPS, (videoW, videoH))
        # 画像を重ね合わせることで動画の作成
        for img in imgList:
            video.write(img)
        # 動画の出力
        video.release()

