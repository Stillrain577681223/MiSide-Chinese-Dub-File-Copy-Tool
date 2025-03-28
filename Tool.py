import os
import time
import ctypes
import shutil
import re
from pathlib import Path
import filecmp

# 检查是否以管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 获取当前电脑的用户名
username = os.getlogin()

# 定义桌面和下载文件夹的路径
def get_desktop_path():
    return Path(fr"C:\Users\{username}\Desktop")

def get_downloads_path():
    return Path(fr"C:\Users\{username}\Downloads")

# 定义要跳过的目录
excluded_directories = [
    fr"C:\Windows",
    fr"C:\Users\{username}\AppData"
]

# 在指定目录及其子目录中查找目标文件夹
def find_folder(folder_name, start_path):
    for root, dirs, files in os.walk(start_path):
        # 跳过指定的排除目录
        if any(root.startswith(excluded) for excluded in excluded_directories):
            dirs[:] = []  # 清空当前目录下的子目录列表，避免进入
            continue
        if folder_name in dirs:
            return os.path.join(root, folder_name)
    return None

# 在指定目录及其子目录中查找目标文件
def find_file_everywhere(file_name, start_path):
    for root, dirs, files in os.walk(start_path):
        # 跳过指定的排除目录
        if any(root.startswith(excluded) for excluded in excluded_directories):
            dirs[:] = []  # 清空当前目录下的子目录列表，避免进入
            continue
        if file_name in files:
            return os.path.join(root, file_name)
    return None

# 全盘扫描
def full_disk_scan(file_name):
    drives = [f"{drive}:\\" for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:\\")]
    for drive in drives:
        print(f"正在扫描驱动器：{drive}")
        file_path = find_file_everywhere(file_name, drive)
        if file_path:
            print(f"在全盘扫描中找到文件：{file_path}")
            return file_path
    return None

# 使用正则表达式查找文件夹
def find_folder_regex(pattern, start_path):
    regex = re.compile(pattern)
    for root, dirs, files in os.walk(start_path):
        # 跳过指定的排除目录
        if any(root.startswith(excluded) for excluded in excluded_directories):
            dirs[:] = []  # 清空当前目录下的子目录列表，避免进入
            continue
        for dir_name in dirs:
            if regex.search(dir_name):
                return os.path.join(root, dir_name)
    return None

# 检查目录中是否存在指定文件
def check_files_in_directory(directory, files_to_check):
    for file_name in files_to_check:
        if not find_file_everywhere(file_name, directory):
            return False
    return True

# 比较两个文件夹的内容
def compare_folders(folder1, folder2):
    comparison = filecmp.dircmp(folder1, folder2)
    if comparison.left_only or comparison.right_only or comparison.diff_files:
        return False  # 文件夹内容不一致
    return True  # 文件夹内容一致

if __name__ == "__main__":
    # 检查是否以管理员权限运行
    if not is_admin():
        is_admin
    target_folder_name = "MiSide"  # 目标文件夹名称
    target_file_name = "MiSideFull.exe"  # 目标文件名称
    additional_files = ["UnityCrashHandler64.exe", "UnityPlayer.dll"]  # 需要检查的额外文件
    chinese_voice_pattern = r"Chinese Voice"  # 正则表达式模式

    # 定义所有要查找的目录
    search_directories = [
        fr"A:\Program Files (x86)\Steam\steamapps\common",
        fr"A:\Program Files\Steam\steamapps\common",
        fr"B:\Program Files (x86)\Steam\steamapps\common",
        fr"B:\Program Files\Steam\steamapps\common",
        fr"C:\Program Files (x86)\Steam\steamapps\common",
        fr"C:\Program Files\Steam\steamapps\common",
        fr"D:\Program Files (x86)\Steam\steamapps\common",
        fr"D:\Program Files\Steam\steamapps\common",
        fr"E:\Program Files (x86)\Steam\steamapps\common",
        fr"E:\Program Files\Steam\steamapps\common",
        fr"F:\Program Files (x86)\Steam\steamapps\common",
        fr"F:\Program Files\Steam\steamapps\common",
        fr"G:\Program Files (x86)\Steam\steamapps\common",
        fr"G:\Program Files\Steam\steamapps\common",
        fr"H:\Program Files (x86)\Steam\steamapps\common",
        fr"H:\Program Files\Steam\steamapps\common",
        fr"I:\Program Files (x86)\Steam\steamapps\common",
        fr"I:\Program Files\Steam\steamapps\common",
        fr"A:\SteamLibrary\steamapps\common",
        fr"B:\SteamLibrary\steamapps\common",
        fr"C:\SteamLibrary\steamapps\common",
        fr"D:\SteamLibrary\steamapps\common",
        fr"E:\SteamLibrary\steamapps\common",
        fr"F:\SteamLibrary\steamapps\common",
        fr"G:\SteamLibrary\steamapps\common",
        fr"H:\SteamLibrary\steamapps\common",
        fr"I:\SteamLibrary\steamapps\common"
    ]

    # 在指定目录中查找目标文件夹和文件
    folder_path = None
    file_path = None
    for directory in search_directories:
        print(f"正在查找目录：{directory}")
        folder_path = find_folder(target_folder_name, directory)
        if folder_path:
            print(f"找到文件夹：{folder_path}")
            file_path = find_file_everywhere(target_file_name, folder_path)
            if file_path:
                print(f"在文件夹中找到文件：{file_path}")
                break
            else:
                print(f"在文件夹 {folder_path} 中未找到文件 {target_file_name}")
        else:
            print(f"未找到文件夹：{target_folder_name} 在目录 {directory}")

    # 如果未找到文件夹，单独查找文件
    if not folder_path:
        print("未找到目标文件夹，正在全盘单独查找文件...")
        file_path = full_disk_scan(target_file_name)

    # 如果找到了文件，检查目录中是否存在额外的文件
    if file_path:
        file_directory = os.path.dirname(file_path)
        if check_files_in_directory(file_directory, additional_files):
            print("已检测到游戏目录，正在查找并复制 'Chinese Voice' 文件夹...")
            current_directory = os.getcwd()
            chinese_voice_folder = find_folder_regex(chinese_voice_pattern, current_directory)
            if chinese_voice_folder:
                print(f"找到 'Chinese Voice' 文件夹：{chinese_voice_folder}")
                # 将文件夹复制到游戏目录下的\Data\LanguagesVoice路径
                target_directory = os.path.join(file_directory, "Data", "LanguagesVoice")
                os.makedirs(target_directory, exist_ok=True)  # 确保目标路径存在

                # 比较文件夹内容
                if os.path.exists(target_directory) and compare_folders(chinese_voice_folder, target_directory):
                    print(f"'Chinese Voice' 文件夹内容已存在且一致，无需复制。")
                else:
                    shutil.copytree(chinese_voice_folder, os.path.join(target_directory, os.path.basename(chinese_voice_folder)), dirs_exist_ok=True)
                    print(f"'Chinese Voice' 文件夹已复制到 {target_directory}")

                print("程序将在30秒内自动退出。")
                time.sleep(30)
                print("程序已退出。")
                exit(0)
            else:
                print("未找到 'Chinese Voice' 文件夹，程序将在30秒内自动退出。")
                time.sleep(30)
                print("程序已退出。")
                exit(0)
        else:
            print("未找到所有必要的文件，程序将在30秒内自动退出。")
            time.sleep(30)
            print("程序已退出。")
            exit(0)

    # 如果未找到文件夹且未找到文件，询问用户是否需要手动输入目录
    user_input = input("未找到游戏目录和文件。是否需要手动输入目录位置？(如果有目录位置，请直接输入在这里，如果没有请键入“否”)：").strip()
    if user_input.lower() != "否":
        custom_directory = user_input
        file_path = find_file_everywhere(target_file_name, custom_directory)
        if file_path:
            print("已检测到游戏目录，正在查找并复制 'Chinese Voice' 文件夹...")
            current_directory = os.getcwd()
            chinese_voice_folder = find_folder_regex(chinese_voice_pattern, current_directory)
            if chinese_voice_folder:
                print(f"找到 'Chinese Voice' 文件夹：{chinese_voice_folder}")
                # 将文件夹复制到游戏目录下的\Data\LanguagesVoice路径
                target_directory = os.path.join(os.path.dirname(file_path), "Data", "LanguagesVoice")
                os.makedirs(target_directory, exist_ok=True)  # 确保目标路径存在

                # 比较文件夹内容
                if os.path.exists(target_directory) and compare_folders(chinese_voice_folder, target_directory):
                    print(f"'Chinese Voice' 文件夹内容已存在且一致，无需复制。")
                else:
                    shutil.copytree(chinese_voice_folder, os.path.join(target_directory, os.path.basename(chinese_voice_folder)), dirs_exist_ok=True)
                    print(f"'Chinese Voice' 文件夹已复制到 {target_directory}")

                print("程序将在30秒内自动退出。")
                time.sleep(30)
                print("程序已退出。")
                exit(0)
            else:
                print("未找到 'Chinese Voice' 文件夹，程序将在30秒内自动退出。")
                time.sleep(30)
                print("程序已退出。")
                exit(0)
    else:
        print("未检测到游戏目录且用户未输入目录，程序将在30秒内自动退出。")
        time.sleep(30)
        print("程序已退出。")
        exit(0)
