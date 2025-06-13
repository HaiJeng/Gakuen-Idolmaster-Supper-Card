import openpyxl
from openpyxl.utils import get_column_letter
import json

# 加载工作簿
wb = openpyxl.load_workbook('../mnt/支援卡-6.9新卡追加.xlsx')

# 获取指定工作表
sheet = wb['持有情况']


def contains_japanese(text):
    # 平假名范围: U+3040 - U+309F
    # 片假名范围: U+30A0 - U+30FF
    for char in text:
        if ('ぁ' <= char <= 'ゔ') or ('ァ' <= char <= 'ヴ'):
            return True
    return False


data = {}
for row in range(1, sheet.max_row + 1):
    for col in range(1, sheet.max_column + 1):
        value = sheet.cell(row=row, column=col).value
        if value is not None and value != '' and contains_japanese(value):
            print(value)
# 保存为JSON文件
# json_path = '持有情况_数值和公式.json'
# with open(json_path, 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
