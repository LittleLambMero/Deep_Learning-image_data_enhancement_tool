"""
資料強化：圖像雜訊處理，可使用「白雜訊」和「高斯雜訊」和「椒鹽雜訊」
"""

import cv2
import numpy as np


def whiteNoise(image: cv2.typing.MatLike, minNoise: int, maxNoise: int):
    """
    對圖片進行白雜訊處理。
    :param image: 圖片
    :param minNoise: 最小雜訊值
    :param maxNoise: 最大雜訊值
    :return: 覆蓋白雜訊之後的圖片
    """
    img = np.copy(image)
    noise = np.random.randint(minNoise, maxNoise, img.shape)
    return np.clip(img + noise, 0, 255).astype('uint8')


def saltPepperNoise(image: cv2.typing.MatLike, fraction: float = 0.1, proportion_SaltPepper: float = 0.5):
    """
    對圖片進行椒鹽雜訊處理。
    :param image: 圖片
    :param fraction: 椒鹽雜訊佔圖片的總比例。預設為 0.1 (10%)
    :param proportion_SaltPepper: 胡椒雜訊與鹽雜訊的比例。預設為 0.5 (50%)
    :return: 覆蓋椒鹽雜訊之後的圖片
    """
    img = np.copy(image)
    size = img.size
    fraction = np.clip(fraction, 0, 1)
    num_salt = np.ceil(fraction * size * proportion_SaltPepper).astype('int')
    num_pepper = np.ceil(fraction * size * (1 - proportion_SaltPepper)).astype('int')
    (row, column) = image.shape[:2]

    # 隨機的座標點
    x = np.random.randint(0, column - 1, num_pepper)
    y = np.random.randint(0, row - 1, num_pepper)
    # 撒胡椒
    img[y, x] = 0

    # 隨機的座標點
    x = np.random.randint(0, column - 1, num_salt)
    y = np.random.randint(0, row - 1, num_salt)
    # 撒鹽
    img[y, x] = 255
    # 好ㄉ，可以吃了咩噗（阿姆阿姆阿姆
    return img


def gaussianNoise(image, mean: float = 0, sigma: float = 1):
    """
    對圖片進行高斯雜訊處理。
    :param image: 圖片
    :param mean: 常態分佈 - 平均值
    :param sigma: 常態分佈 - 標準差
    :return: 覆蓋高斯雜訊之後的圖片
    """
    img = np.copy(image)
    noise = np.random.normal(mean, sigma, img.shape)
    return np.clip(img + noise, 0, 255).astype('uint8')
