# 代码生成时间: 2025-09-01 22:43:50
# sorting_algorithms.py

"""
Sorting Algorithms module providing various sorting methods in Python.
"""

from typing import List


class SortingAlgorithms:
    """
    Class containing methods for different sorting algorithms.
    """
    
    def __init__(self):
        pass

    def bubble_sort(self, arr: List[int]) -> List[int]:
        """
        Sorts an array using the Bubble Sort algorithm.
        
        Args:
            arr (List[int]): The list of integers to be sorted.
        
        Returns:
            List[int]: The sorted list of integers.
        """
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def selection_sort(self, arr: List[int]) -> List[int]:
        """
        Sorts an array using the Selection Sort algorithm.
        
        Args:
            arr (List[int]): The list of integers to be sorted.
        
        Returns:
            List[int]: The sorted list of integers.
        """
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[min_idx] > arr[j]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    def insertion_sort(self, arr: List[int]) -> List[int]:
        """
        Sorts an array using the Insertion Sort algorithm.
        
        Args:
            arr (List[int]): The list of integers to be sorted.
        
        Returns:
            List[int]: The sorted list of integers.
        """
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    def merge_sort(self, arr: List[int]) -> List[int]:
        """
        Sorts an array using the Merge Sort algorithm.
        
        Args:
            arr (List[int]): The list of integers to be sorted.
        
        Returns:
            List[int]: The sorted list of integers.
        """
        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]
            R = arr[mid:]
            
            self.merge_sort(L)
            self.merge_sort(R)
            
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
        return arr

# Example usage
if __name__ == '__main__':
    alg = SortingAlgorithms()
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print("Original array: ", test_array)
    print("Sorted array (Bubble Sort): ", alg.bubble_sort(test_array.copy()))
    print("Sorted array (Selection Sort): ", alg.selection_sort(test_array.copy()))
    print("Sorted array (Insertion Sort): ", alg.insertion_sort(test_array.copy()))
    print("Sorted array (Merge Sort): ", alg.merge_sort(test_array.copy()))