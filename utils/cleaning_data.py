'''
This file is created to clean the data and convert it to the required format.
'''

# ----------------------- Modules -------------------------------- #
import re
import pandas as pd


# -------------------- Data Conversion --------------------------- #
def clean_and_convert(column_data):
    cleaned_data = []
    for item in column_data:
        if pd.notna(item):
            match = re.search(r'\d+(\.\d+)?', str(item))
            if match:
                value_str = match.group()
                if '.' in value_str:
                    value = float(value_str)
                else:
                    value = int(value_str)
                cleaned_data.append(value)
            else:
                cleaned_data.append(0.0)  # Handle cases where no numeric value is found
        else:
            cleaned_data.append(0)  # Handle missing values
    return cleaned_data
