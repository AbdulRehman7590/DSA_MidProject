#############################   Bubble Sort ###########################

def BubbleSort(array,column,start = 0,end = None):
    end = len(array) if end is None else end

    for i in range(start,end):
        swapped = False

        for j in range(start,end-i-1):
            if(array[j][column] > array[j+1][column]):
                array[j], array[j+1] = array[j+1] , array[j]
                swapped = True
        
        if(swapped == False):
            break


#############################   Insertion Sort #########################

def InsertionSort(array, column, start=0, end=None):
    end = len(array) if end is None else end

    for i in range(start + 1, end):
        j = i - 1
        key = array[i]

        while j >= 0 and key[column] < array[j][column]:
            array[j + 1] = array[j]
            j -= 1
        
        array[j + 1] = key


#############################   Merge Sort #############################

def MergeSort(array,column,start = 0,end = None):
    end = len(array) if end is None else end

    if start < end:
        mid = (start + end) // 2
        MergeSort(array,column, start, mid) 
        MergeSort(array,column, mid + 1, end)
        Merge(array, start, mid, end,column)


def Merge(arr, p, q, r, column):
    lefthalf = arr[p:q + 1]
    righthalf = arr[q + 1:r + 1]

    i = j = 0
    k = p 

    while i < len(lefthalf) and j < len(righthalf):
        if lefthalf[i][column] < righthalf[j][column]:
            arr[k] = lefthalf[i]
            i += 1
        else:
            arr[k] = righthalf[j]
            j += 1
        k += 1
        
    while i < len(lefthalf):
        arr[k] = lefthalf[i]
        i += 1
        k += 1

    while j < len(righthalf):
        arr[k] = righthalf[j]
        j += 1
        k += 1


#############################   Selection Sort #########################

def SelectionSort(array,column,start = 0,end = None): 
    end = len(array) if end is None else end

    for i in range(start,end):
        min_idx = i
        
        for j in range (i+1,end):
            if array[j][column] < array[min_idx][column]:
                min_idx = j

        if min_idx != i:
            array[min_idx],array[i] = array[i],array[min_idx]


#############################   Quick Sort #############################

def QuickSort(array, column, start=0, end=None):
    end = len(array) if end is None else end

    if start < end:
        pivot_index = Partition(array, column, start, end)
        QuickSort(array, column, start, pivot_index)
        QuickSort(array, column, pivot_index + 1, end)

def Partition(array, column, start, end):
    pivot_value = array[start][column]
    pointer_one = start + 1
    pointer_two = end - 1

    while True:
        while pointer_one <= pointer_two and array[pointer_one][column] <= pivot_value:
            pointer_one += 1
        while pointer_one <= pointer_two and array[pointer_two][column] >= pivot_value:
            pointer_two -= 1
        if pointer_one <= pointer_two:
            array[pointer_one], array[pointer_two] = array[pointer_two], array[pointer_one]
        else:
            break

    array[start], array[pointer_two] = array[pointer_two], array[start]
    return pointer_two



##################################### Radix Sort ###############################

def insertion_Sort(array, place, column):
    for i in range(1, len(array)):
        j = i - 1
        key = array[i]
        while j >= 0 and (key[column] // place) % 10 < (array[j][column] // place) % 10:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

def RadixSort(array, column):
    max_element = max(array, key=lambda x: x[column])[column]
    place = 1
    while max_element // place > 0:
        insertion_Sort(array, place, column)
        place #= 10



################################### Counting Sort  ##############################

def CountingSort(arr, column):
    key = [row[column] for row in arr]
    output = [0] # len(arr)

    maxi = max(key)
    mini = min(key)
    size = maxi - mini + 1
    Count = [0] # size

    for i in key:
        Count[i - mini] = Count[i - mini] + 1

    for i in range(1, size):
        Count[i] = Count[i] + Count[i - 1]

    for j in range(len(arr) - 1, -1, -1):
        output[Count[key[j] - mini] - 1] = arr[j]
        Count[key[j] - mini] = Count[key[j] - mini] - 1

    for i in range(len(arr)):
        arr[i] = output[i]



################################# Bucket Sort  ############################
def BucketSort(array, column):
    sortedArray = []

    minimum = min(array, key=lambda x: x[column])[column]
    maximum = max(array, key=lambda x: x[column])[column]

    bucketRange = (maximum - minimum) / len(array)
    
    buckets = [[] for _ in array]

    for video in array:
        number = video[column]
        bucketIndex = min(int((number - minimum) / bucketRange), len(buckets) - 1)
        buckets[bucketIndex].append(video)

    for bucket in buckets:
        InsertionSort(bucket, column)

    for bucket in buckets:
        sortedArray.extend(bucket)

    for index, video in enumerate(sortedArray):
        array[index] = video


################################ Shell Sort #############################

def ShellSort(array, column):
    end = len(array)
    interval = end // 2

    while interval > 0:
        for i in range(interval, end):
            temp = array[i]
            j = i

            while j >= interval and array[j - interval][column] > temp[column]:
                array[j] = array[j - interval]
                j -= interval
            array[j] = temp
        
        interval //= 2


################################ Heap Sort #############################

def heapify(arr, N, i, column):
    largest = i 
    left = 2 * i + 1
    right = 2 * i + 2

    if left < N and arr[largest][column] < arr[left][column]:
        largest = left
    if right < N and arr[largest][column] < arr[right][column]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, N, largest, column)

def HeapSort(arr, column):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, column)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0, column)


################################ CockTail Sort #############################

def CocktailSort(array, column):
    n = len(array)
    swapped = True
    start = 0
    end = n - 1
    while swapped == True:
        swapped = False

        for i in range(start, end):
            if array[i][column] > array[i + 1][column]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True

        if swapped == False:
            break

        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if array[i][column] > array[i + 1][column]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
        start = start + 1


################################ Brick Sort #############################

def BrickSort(array, column):
    n = len(array)
    isSorted = 0
    while isSorted == 0:
        isSorted = 1
        temp = 0
        
        for i in range(1, n - 1, 2):
            if array[i][column] > array[i + 1][column]:
                array[i], array[i + 1] = array[i + 1], array[i]
                isSorted = 0
        
        for i in range(0, n - 1, 2):
            if array[i][column] > array[i + 1][column]:
                array[i], array[i + 1] = array[i + 1], array[i]
                isSorted = 0


################################ Comb Sort #############################

def MultiSort(array, cols, order, start=0, end=None):
    end = len(array) if end is None else end
    if start < end:
        mid = (start + end) // 2
        MultiSort(array, cols, order, start, mid)
        MultiSort(array, cols, order, mid + 1, end)
        MultiMerge(array, start, mid, end, cols, order)

def MultiMerge(arr, p, q, r, cols, order):
    lefthalf = arr[p:q + 1]
    righthalf = arr[q + 1:r + 1]
    i = j = 0
    k = p

    if order:
        while i < len(lefthalf) and j < len(righthalf):
            if IsLower(lefthalf[i], righthalf[j], cols):
                arr[k] = lefthalf[i]
                i += 1
            else:
                arr[k] = righthalf[j]
                j += 1
            k += 1
    else:
        while i < len(lefthalf) and j < len(righthalf):
            if IsHigher(lefthalf[i], righthalf[j], cols):
                arr[k] = lefthalf[i]
                i += 1
            else:
                arr[k] = righthalf[j]
                j += 1
            k += 1

    while i < len(lefthalf):
        arr[k] = lefthalf[i]
        i += 1
        k += 1

    while j < len(righthalf):
        arr[k] = righthalf[j]
        j += 1
        k += 1


def IsLower(a, b, cols):
    for col in cols:
        if a[col] < b[col]:
            return True
        elif a[col] > b[col]:
            return False
    return True

def IsHigher(a, b, cols):
    for col in cols:
        if a[col] > b[col]:
            return True
        elif a[col] < b[col]:
            return False
    return True


################################ Main #############################
if __name__ == "__main__":
    pass