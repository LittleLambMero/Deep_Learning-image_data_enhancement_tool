"""
資料強化：圖像模糊化處理，可以使用平均模糊與高斯模糊
"""

import cv2


def imageBlur(image: cv2.typing.MatLike, kernelSize: int = 5):
    """
    將圖像按照像素模糊尺寸進行模糊化處理。計算指定區域所有像素的平均值，再將平均值取代中心像素，
    :param image: 圖片
    :param kernelSize: 指定區域單位。指定區域單位設定的範圍越大，則模糊的效果越明顯
    :return: 進行模糊處理後的圖片
    """
    if kernelSize < 0:
        kernelSize = 1

    return cv2.blur(image, (kernelSize, kernelSize))


def imageGaussianBlur(image: cv2.typing.MatLike, kernelSize: int = 5):
    """
    使用高斯分佈進行模糊化的計算，指定模糊區域單位（必須是大於 1 的奇數）後就能產生不同程度的模糊效果。
    :param image: 圖片
    :param kernelSize: 指定模糊區域單位（必須是大於 1 的奇數）
    :return: 進行模糊處理後的圖片
    """
    if kernelSize < 0:
        kernelSize = 1

    if kernelSize % 2 == 0:
        kernelSize -= 1

    return cv2.GaussianBlur(image, (kernelSize, kernelSize), sigmaX=0, sigmaY=0)
