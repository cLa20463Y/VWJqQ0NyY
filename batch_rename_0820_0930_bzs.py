# 代码生成时间: 2025-08-20 09:30:40
import os
import glob
from typing import List

"""
批量文件重命名工具
"""
def rename_files(directory: str, pattern: str, replacement: str) -> List[str]:
    """
    在指定目录中批量重命名匹配特定模式的文件。

    :param directory: 要重命名文件的目录
    :param pattern: 要替换的文件名模式
    :param replacement: 替换后的模式
    :return: 重命名的文件列表
    """
    # 获取指定目录下所有匹配的文件
    files = glob.glob(os.path.join(directory, f'*{pattern}*'))
    renamed_files = []
    for file in files:
        try:
            # 构造新的文件名
            new_name = file.replace(pattern, replacement)
            # 重命名文件
            os.rename(file, new_name)
            renamed_files.append(new_name)
        except OSError as e:
            print(f'Error renaming {file}: {e}')
    return renamed_files


def main():
    """
    程序的主入口点。
    """
    directory = input('Enter the directory path: ')
    pattern = input('Enter the pattern to replace: ')
    replacement = input('Enter the replacement pattern: ')
    try:
        renamed_files = rename_files(directory, pattern, replacement)
        print('Renamed files:')
        for file in renamed_files:
            print(file)
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()