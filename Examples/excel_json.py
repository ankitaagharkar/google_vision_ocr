import json
import sys

import xlrd


workbook = xlrd.open_workbook(r"C:\Users\ankitaa\Desktop\State_wise_filtering.xlsx")
worksheet = workbook.sheet_by_index(0)

data = []
keys = [v.value for v in worksheet.row(0)]
for row_number in range(worksheet.nrows):
    if row_number == 0:
        continue
    row_data = {}
    for col_number, cell in enumerate(worksheet.row(row_number)):
        row_data[keys[col_number]] = cell.value
    data.append(row_data)

with open('../config/filtering.json', 'w') as json_file:
    json_file.write(json.dumps({'data': data}))