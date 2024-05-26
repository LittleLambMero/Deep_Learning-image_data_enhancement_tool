import math
import os

import cv2

import 圖像旋轉 as tool_Rotate
import 圖像拉伸 as tool_Stretch
import 圖像亮度與對比度 as tool_BCAdjust
import 圖像模糊化 as tool_Blur
import 圖像雜訊 as tool_Noise

import 參數組態 as Config


def readList(alist: list[str]):
    print("************")
    for obj in alist:
        print(obj)

    print("************")


def transferToRealPath(dataset_list: list[str], root_path: str):
    for i in range(0, len(dataset_list)):
        dataset_list[i] = os.path.join(root_path, dataset_list[i])


def recursiveGetFile(path_list: list[str], file_extension: str) -> list[str]:
    """
    遞歸取得完整資料夾下的所有指定副檔名的檔案路徑。
    :param path_list: 包含了檔案路徑的列表
    :param file_extension: 檔案的副檔名，不符合該值的檔案都會被忽略
    :return: 檔案路徑列表
    """
    file_list = []
    for path in path_list:
        if os.path.isdir(path):
            dir_list = os.listdir(path)
            transferToRealPath(dir_list, path)
            temp = recursiveGetFile(dir_list, file_extension)
            for p in temp:
                file_list.append(p)
        else:
            file_list.append(path)

    shadow_list = file_list.copy()
    for path in shadow_list:
        file_name = os.path.basename(path)
        if not file_name.split(".")[-1] == file_extension:
            file_list.remove(path)

    return file_list


def listDirFiles(dir_path: str):
    file_list = []
    if os.path.isdir(dir_path):
        for f in os.listdir(dir_path):
            file_list.append(f)

        transferToRealPath(file_list, dir_path)

    return file_list


def contain(obj, obj_list: list):
    """
    檢測一個列表中是否包含指定物件。
    :param obj: 任意物件
    :param obj_list: 列表
    :return: 如果物件存在列表之中，返回 True，否則返回 False
    """
    for element in obj_list:
        if obj == element:
            return True

    return False


def reloadingDataset(dataset_rootpath: str, file_extension: str):
    re_dataset = os.listdir(dataset_rootpath)
    transferToRealPath(re_dataset, temp_dataset_path)
    return recursiveGetFile(re_dataset, file_extension)


def saveImg(image: cv2.typing.MatLike, f_path: str, prefix: str):
    new_file_name = os.path.basename(f_path).split(".")[0]
    if not new_file_name.startswith("[emh]"):
        new_file_name = "[emh]" + new_file_name

    new_file_name += prefix + "." + Config.file_extension_limit
    cv2.imwrite(os.path.join(os.path.split(f_path)[0], new_file_name), image)


def run_rotation(file_list: list[str]):
    for f in file_list:
        f_name = os.path.basename(f)
        if not Config.is_multiple_argumentation:
            if f_name.startswith("[emh]"):
                continue

        if f_name.count("_rt") > 0:
            continue

        img = cv2.imread(f)
        for angle in range(math.floor(Config.rotated_angle), 360, math.floor(Config.rotated_angle)):
            img = tool_Rotate.imageRotation(img, angle, Config.color_filled)
            saveImg(img, f, "_rt" + str(angle))


def run_stretch(file_list: list[str]):
    for f in file_list:
        f_name = os.path.basename(f)
        if not Config.is_multiple_argumentation:
            if f_name.startswith("[emh]"):
                continue

        if (f_name.count("_ws-x") + f_name.count("_hs-x") + f_name.count("_zoomed-x")) > 0:
            continue

        img = cv2.imread(f)
        if Config.stretch_type[0] == 1:
            img = tool_Stretch.widthStretch(img, Config.stretch_scale)
            saveImg(img, f, "_ws-x" + str(Config.stretch_scale))

        if Config.stretch_type[1] == 1:
            img = tool_Stretch.heightStretch(img, Config.stretch_scale)
            saveImg(img, f, "_hs-x" + str(Config.stretch_scale))

        if Config.stretch_type[2] == 1:
            img = tool_Stretch.imageZoomed(img, Config.stretch_scale)
            saveImg(img, f, "_zoomed-x" + str(Config.stretch_scale))


def run_BCAdjust(file_list: list[str]):
    for f in file_list:
        f_name = os.path.basename(f)
        if not Config.is_multiple_argumentation:
            if f_name.startswith("[emh]"):
                continue

        if (f_name.count("_brt") + f_name.count("_cont") + f_name.count("_br-ct")) > 0:
            continue

        img = cv2.imread(f)
        if Config.adjustment_type[0] == 1:
            img = tool_BCAdjust.brightnessAdjustment(img, Config.brightness_value)
            saveImg(img, f, "_brt" + str(Config.brightness_value))

        if Config.adjustment_type[1] == 1:
            img = tool_BCAdjust.contrastAdjustment(img, Config.contrast_value)
            saveImg(img, f, "_cont" + str(Config.contrast_value))

        if Config.adjustment_type[2] == 1:
            img = tool_BCAdjust.allAdjustment(img, Config.brightness_value, Config.contrast_value)
            saveImg(img, f, "_br-ct" + str(Config.brightness_value))


def run_blur(file_list: list[str]):
    for f in file_list:
        f_name = os.path.basename(f)
        if not Config.is_multiple_argumentation:
            if f_name.startswith("[emh]"):
                continue

        if (f_name.count("_blur") + f_name.count("_gblur")) > 0:
            continue

        img = cv2.imread(f)
        b_type = Config.blur_type.upper()
        if b_type == "B":
            img = tool_Blur.imageBlur(img, Config.kernel_size)
            saveImg(img, f, "_blur-k" + str(Config.kernel_size))

        elif b_type == "G":
            img = tool_Blur.imageGaussianBlur(img, Config.kernel_size)
            saveImg(img, f, "_gblur-k" + str(Config.kernel_size))

        else:
            raise ValueError("參數只接受「B」或「G」")


def run_noise(file_list: list[str]):
    for f in file_list:
        f_name = os.path.basename(f)
        if not Config.is_multiple_argumentation:
            if f_name.startswith("[emh]"):
                continue

        if (f_name.count("_wn") + f_name.count("_spn") + f_name.count("_gn")) > 0:
            continue

        img = cv2.imread(f)
        noise_type = Config.noise_type.upper()
        if noise_type == "W":
            min_noise, max_noise = Config.WNoise_noise_value
            img = tool_Noise.whiteNoise(img, min_noise, max_noise)
            saveImg(img, f, "_wn-" + str(min_noise) + "~" + str(max_noise))

        elif noise_type == "SP":
            img = tool_Noise.saltPepperNoise(img, Config.SPNoise_fraction, Config.SPNoise_proportion)
            saveImg(img, f, "_spn-frac" + str(Config.SPNoise_fraction) + "-prop" + str(Config.SPNoise_proportion))

        elif noise_type == "G":
            img = tool_Noise.gaussianNoise(img, Config.GNoise_mean, Config.GNoise_sigma)
            saveImg(img, f, "_gn-mean" + str(Config.GNoise_mean) + "-sigma" + str(Config.GNoise_sigma))

        else:
            raise ValueError("參數只接受「W」、「SP」或「G」")


temp_dataset_path = ''

if not os.path.exists(Config.dataset_path):
    raise FileNotFoundError("找不到資料集！")

if not len(Config.train_dir_name) == 0:
    temp_dataset_path = str(os.path.join(Config.dataset_path, Config.train_dir_name))
    if not os.path.exists(temp_dataset_path):
        raise FileNotFoundError("找不到測試集！")

else:
    temp_dataset_path = Config.dataset_path

dataset = os.listdir(temp_dataset_path)
transferToRealPath(dataset, temp_dataset_path)
if Config.whitelist:
    if len(Config.class_whitelist) == 0:
        raise ValueError("啟用白名單的模式下，白名單列表不可為空列表。")

    dataset_copy = dataset.copy()
    for file in dataset_copy:
        if not os.path.isdir(file):
            dataset.remove(file)
            continue

        dir_name = os.path.basename(file)
        if not contain(dir_name, Config.class_whitelist):
            dataset.remove(file)

if not (Config.file_extension_limit == "jpg" or
        Config.file_extension_limit == "jpeg" or
        Config.file_extension_limit == "png"):
    raise ValueError("副檔名只能是「jpg」、「jpeg」、「png」的其中一種")

image_list = recursiveGetFile(dataset, Config.file_extension_limit)
image_old_count = len(image_list)
if image_old_count == 0:
    raise IOError("圖片載入失敗！")

print("********** 開始進行資料強化 **********")

if Config.processed_Rotation:
    print("開始進行「圖像旋轉」強化...")
    run_rotation(image_list)
    print("完成")

if Config.is_multiple_argumentation:
    image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)

if Config.processed_Stretch:
    print("開始進行「圖像拉伸」強化...")
    run_stretch(image_list)
    print("完成")

if Config.is_multiple_argumentation:
    image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)

if Config.processed_BCAdjustment:
    print("開始進行「圖像明暗對比」強化...")
    run_BCAdjust(image_list)
    print("完成")

if Config.is_multiple_argumentation:
    image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)

if Config.processed_Blur:
    print("開始進行「圖像模糊」強化...")
    run_blur(image_list)
    print("完成")

if Config.is_multiple_argumentation:
    image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)

if Config.processed_Noise:
    print("開始進行「圖像雜訊」強化...")
    run_noise(image_list)
    print("完成")

print("********** 資料強化完成 **********")
print("統計中...")
image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)
image_new_count = len(image_list)
increased_count = image_new_count - image_old_count
increased_rate = float(image_new_count) / float(image_old_count)
print("總計資料數量：" + str(image_new_count))
print("圖片數量增加 " + str(increased_count))
print("上升比率：" + str(increased_rate))
