"""
資料強化：調整圖片的亮度與對比度。
"""
import cv2
import numpy as np


def brightnessAdjustment(image: cv2.typing.MatLike, value: int = 0):
    """
    調整圖片亮度。
    :param image: 圖片
    :param value: 要調整的亮度值。數值越大圖片越亮，反之則越暗
    :return: 修正完成的圖片
    """
    return allAdjustment(image, value, 0)


def contrastAdjustment(image: cv2.typing.MatLike, value: int = 0):
    """
    調整圖片對比度。
    :param image: 圖片
    :param value: 要調整的對比度。數值越大圖片色彩對比越強烈，反之則越微弱
    :return: 修正完成的圖片
    """
    return allAdjustment(image, 0, value)


def allAdjustment(image: cv2.typing.MatLike, brightness: int = 0, contrast: int = 0):
    """
    調整圖片的亮度與對比度。
    :param image: 圖片
    :param brightness: 要調整的亮度值。數值越大圖片越亮，反之則越暗
    :param contrast: 要調整的對比度。數值越大圖片色彩對比越強烈，反之則越微弱
    :return: 修正完成的圖片
    """
    output = image * (contrast / 127 + 1) - contrast + brightness
    output = np.clip(output, 0, 255)
    output = np.uint8(output)

    return output
