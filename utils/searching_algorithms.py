# ----------------------- Modules -------------------------------- #
from enum import Enum


# ----------------------- Classes -------------------------------- #
class FilterType(Enum):
        CONTAINS = 1
        STARTS_WITH = 2
        ENDS_WITH = 3


# ---------------------- Linear searching ------------------------ #
def LinearSearch(df, columnName, search_key, filter_type):
        indexList = []
        for index, value in enumerate(df):
            row = str(value[columnName])
            if filter_type == 1 and search_key in row:
                indexList.append(value)
            elif filter_type == 2 and row.endswith(search_key):
                indexList.append(value)
            elif filter_type == 3 and row.startswith(search_key):
                indexList.append(value)
        
        return indexList


# ---------------------- Binary searching ------------------------ #
def MultiLinearSearch(df, col, key, filter_Type, col1, key2, filter_Type2, operator):
    list_1 = LinearSearch(df, col, key, filter_Type)
    list_2 = LinearSearch(df, col1, key2, filter_Type2)
    # Converting in tuples as we have a list of lists
    list1 = [tuple(sublist) for sublist in list_1]
    list2 = [tuple(sublist) for sublist in list_2]  
    array = []
    if operator == "And":
        array = list(set(list1 + list2))
    elif operator == "Or":
        array = list(set(list1) & set(list2))
    elif operator == "Not":
        array = list(set(list1) - set(list2))   
    array = [list(subtuple) for subtuple in array]   
    return array


# ---------------------- Data filters ------------------------ #
def starts_With(value, search_key):
        size = len(str(search_key))
        for i in range(size):
            if value[i] != search_key[i]:
                return False
        return True

def ends_With(value, search_key):
        n = len(str(search_key))
        for i in range(len(value) - n, len(value)):
            if search_key[i - (len(value) - n)] != value[i]:
                return False
        return True

def contains_With(value, search_key):
    n = len(str(value))
    m = len(search_key)
    for i in range(n - m + 1):
        j = i
        for k in range(m):
            if value[j] != search_key[k]:
                break
            j += 1
        else:
            return True
        return False   





