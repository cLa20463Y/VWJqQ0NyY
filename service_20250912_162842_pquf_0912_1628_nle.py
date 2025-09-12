# 代码生成时间: 2025-09-12 16:28:42
# 文件名: folder_structure_organizer.py
# 程序用途：整理文件夹结构
# 作者：AI助手

from pathlib import Path
from typing import List
import logging


# 设置日志配置
logging.basicConfig(level=logging.INFO)

"""
文件夹结构整理器类
"""
class FolderStructureOrganizer:
    """
    类初始化函数
    :param base_folder: 需要整理的文件夹路径
    """
    def __init__(self, base_folder: str):
        self.base_folder = Path(base_folder)
        if not self.base_folder.exists():
            logging.error(f"Base folder {self.base_folder} does not exist.")
            raise FileNotFoundError(f"Base folder {self.base_folder} does not exist.")
        if not self.base_folder.is_dir():
            logging.error(f"{self.base_folder} is not a directory.")
            raise NotADirectoryError(f"{self.base_folder} is not a directory.")

    """
    整理文件夹结构
    :param structure: 需要整理成的目标结构，格式为列表，包含文件夹名称
    """
    def organize(self, structure: List[str]) -> None:
        logging.info(f"Starting to organize {self.base_folder} into the following structure: {structure}")
        try:
            for folder_name in structure:
                folder_path = self.base_folder / folder_name
                folder_path.mkdir(parents=True, exist_ok=True)
                logging.info(f"Created folder {folder_path}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise


def main():
    import sys
    # 解析命令行参数
    if len(sys.argv) != 3:
        print("Usage: python folder_structure_organizer.py [base_folder_path] [target_structure_json_file]")
        sys.exit(1)
    base_folder_path = sys.argv[1]
    target_structure_json_file = sys.argv[2]

    try:
        # 读取目标结构文件
        with open(target_structure_json_file, 'r') as f:
            target_structure = json.load(f)
    except FileNotFoundError:
        print(f"Target structure file {target_structure_json_file} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from {target_structure_json_file}.")
        sys.exit(1)

    # 创建文件夹结构整理器并整理文件夹
    organizer = FolderStructureOrganizer(base_folder_path)
    organizer.organize(target_structure)

if __name__ == '__main__':
    main()