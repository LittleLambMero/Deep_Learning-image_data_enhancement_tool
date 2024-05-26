"""
資料強化: 2 維圖像旋轉。
"""
import cv2
import numpy as np


def imageRotation(image: cv2.typing.MatLike, angle: float = 90, colorRGB: tuple[int] = (0, 0, 0)):
    """
    對指定圖片進行 2 維固定角度旋轉。

    :param image: 圖片
    :param angle: 旋轉角度, 預設旋轉 90 度
    :param colorRGB: 旋轉後圖片的空白位置色彩, 預設為黑色
    :return: 旋轉後的圖片
    """
    (height, width) = image.shape[:2]
    (centerX, centerY) = (width / 2, height / 2)
    angle = np.clip(angle, 1, 359)

    rotateMtx = cv2.getRotationMatrix2D((centerX, centerY), -angle, 1.0)
    cosTheta = np.abs(rotateMtx[0, 0])
    sinTheta = np.abs(rotateMtx[0, 1])

    newWidth = int((height * sinTheta + width * cosTheta))
    newHeight = int((height * cosTheta + width * sinTheta))

    rotateMtx[0, 2] = rotateMtx[0, 2] + (newWidth / 2) - centerX
    rotateMtx[1, 2] = rotateMtx[1, 2] + (newHeight / 2) - centerY

    return cv2.warpAffine(image, rotateMtx, (newWidth, newHeight), colorRGB)
