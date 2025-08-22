# 代码生成时间: 2025-08-23 03:25:02
import os
from typing import List

"""
Batch Rename Tool
This module provides functionality to rename files in a directory based on a given pattern.
"""

class BatchRenameTool:
    """
# 增强安全性
    A class to handle batch renaming of files in a specified directory.
    """

    def __init__(self, directory: str):
        """
        Initialize the BatchRenameTool with a specified directory.
        :param directory: The directory in which files will be renamed.
        """
        self.directory = directory
# NOTE: 重要实现细节

    def rename_files(self, pattern: str, extension: str = None) -> List[str]:
# TODO: 优化性能
        """
        Rename all files in the directory according to the provided pattern.
        :param pattern: The naming pattern for the files.
        :param extension: The file extension to filter by.
        :return: A list of renamed file paths.
        """
        renamed_files = []
        for filename in os.listdir(self.directory):
            # Check if the file has the specified extension
            if extension and not filename.endswith(extension):
                continue
            # Create a new filename by applying the pattern
            new_filename = f"{pattern}_{os.path.splitext(filename)[0]}{os.path.splitext(filename)[1]}"
            try:
# 改进用户体验
                os.rename(os.path.join(self.directory, filename), os.path.join(self.directory, new_filename))
                renamed_files.append(new_filename)
            except OSError as e:
# NOTE: 重要实现细节
                print(f"Error renaming file {filename}: {e}")
        return renamed_files
# FIXME: 处理边界情况

# Example usage
if __name__ == "__main__":
    directory_path = "/path/to/your/directory"
    rename_tool = BatchRenameTool(directory=directory_path)
# 改进用户体验
    pattern = "new_name"
# 优化算法效率
    extension = ".txt"
    renamed_files = rename_tool.rename_files(pattern=pattern, extension=extension)
    for file in renamed_files:
        print(f"Renamed file to: {file}")