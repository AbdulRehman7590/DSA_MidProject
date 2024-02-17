# ----------------------- Modules -------------------------------- #
from PyQt5.QtCore import QThread
from utils.sorting_algorithms import *

# ----------------------- Classes -------------------------------- #
class SortingThread(QThread):
    def __init__(self, array, column, sort_type, algorithm):
        super().__init__()
        self.array = array
        self.sort_type = sort_type
        self.algorithm = algorithm
        self._column = []

        for col in column:
            if col == "Title":
                self._column.append(0)
            elif col == "Price":
                self._column.append(1)
            elif col == "Seller":
                self._column.append(2)
            elif col == "Sold_Items":
                self._column.append(3)
            elif col == "Country":
                self._column.append(4)
            elif col == "Status":
                self._column.append(5)
            elif col == "Seller_Rank":
                self._column.append(6)
            elif col == "Shipping":
                self._column.append(7)


    # ----------------------- Run -------------------------------- #
    def run(self):
        if self.algorithm == "Bubble Sort":
            BubbleSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()

        elif self.algorithm == "Selection Sort":
            SelectionSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()

        elif self.algorithm == "Merge Sort":
            MergeSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Heap Sort":
            HeapSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Insertion Sort":
            InsertionSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Quick Sort":
            QuickSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Radix Sort":
            RadixSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Count Sort":
            CountingSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Bucket Sort":
            BucketSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Shell Sort":
            ShellSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Brick Sort":
            BrickSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()


        elif self.algorithm == "Cocktail Sort":
            CocktailSort(self.array, column=self._column[0])
            if not self.sort_type:
                    self.array.reverse()

        elif self.algorithm == "Multi Sort":
            MultiSort(self.array, self._column, self.sort_type)

        self.finished.emit()
