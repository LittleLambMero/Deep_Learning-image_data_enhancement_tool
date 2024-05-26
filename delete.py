import os

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

image_list = recursiveGetFile(dataset, Config.file_extension_limit)
image_old_count = len(image_list)
print("********** 開始刪除資料 **********")
for img in image_list:
    if os.path.basename(img).startswith("[emh]"):
        os.unlink(img)

print("********** 資料刪除完成 **********")
print("統計中...")
image_list = reloadingDataset(temp_dataset_path, Config.file_extension_limit)
image_new_count = len(image_list)
decreased_count = image_old_count - image_new_count
print("總計資料數量：" + str(image_new_count))
print("總共刪除 " + str(decreased_count) + " 筆資料")
