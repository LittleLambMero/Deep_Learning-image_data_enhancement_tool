"""
資料強化: 圖像拉伸。對圖片進行拉長、縮短、縮放等尺寸操作
"""
import cv2


def widthStretch(image: cv2.typing.MatLike, scale: float = 1):
    """
    將圖片的寬度依照比例拉伸。
    :param image: 圖片
    :param scale: 拉伸比例，大於 1 時拉長，小於 1 時收縮
    :return: 拉伸後的圖片
    """

    originWidth = image.shape
    return cv2.resize(image, (originWidth[0], int(originWidth[1] * scale)))


def heightStretch(image: cv2.typing.MatLike, scale: float = 1):
    """
    將圖片的高度依照比例拉伸。
    :param image: 圖片
    :param scale: 拉伸比例，大於 1 時拉長，小於 1 時收縮
    :return: 拉伸後的圖片
    """

    originWidth = image.shape
    return cv2.resize(image, (int(originWidth[0] * scale), originWidth[1]))


def imageZoomed(image: cv2.typing.MatLike, scale: float = 1):
    """
    將圖片依照比例放大縮小。
    :param image: 圖片
    :param scale: 縮放比例，大於 1 時放大，小於 1 時縮小
    :return: 縮放後的圖片
    """

    originWidth = image.shape
    return cv2.resize(image, (int(originWidth[0] * scale), int(originWidth[1] * scale)))
