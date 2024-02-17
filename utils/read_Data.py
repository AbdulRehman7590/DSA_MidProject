# --------------------- Modules --------------------------------- #
import csv

# ------------------ Reading a file ----------------------------- #
def read_file(fileName):
    with open(f"Input/{fileName}",'r',encoding='utf-8') as file:
        data = list(csv.reader(file))
        data = data[1:]

    if fileName != "million_data.csv":
        for row in data:
            row[1] = float(row[1])
            row[3] = int(row[3])
            row[7] = float(row[7])
    else:
        for row in data:
            row[1] = float(row[1])
            row[3] = float(row[3])
            row[7] = float(row[7])
    
    return data
