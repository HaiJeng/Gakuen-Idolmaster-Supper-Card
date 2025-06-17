import json

import openpyxl

from model.SupportCard import Rarity
from service.CardCalculator import CardCalculator
from util.ExcelUtil import ExcelUtil
from util.ObjUtil import ObjUtil
from util.StrUtil import StrUtil

"""
用于解析excel的持有情况表，并替换公式，数据保存至resource/card/持有情况_数值和公式
"""

# 加载工作簿
wb = openpyxl.load_workbook('../mnt/支援卡-6.9新卡追加.xlsx')
# 加载词条数据
with open('../resource/tmp/entry_dict.json', 'r', encoding='utf-8') as f:
    entry_data = json.load(f)

"""读取 route_dict.json 文件并返回字典"""
with open('../resource/tmp/route_dict.json', 'r', encoding='utf-8') as f:
    route_data = json.load(f)

# 获取指定工作表
sheet = wb['持有情况']


def contains_japanese(text):
    # 平假名范围: U+3040 - U+309F
    # 片假名范围: U+30A0 - U+30FF
    if text == '':
        return False
    for char in text:
        if ('ぁ' <= char <= 'ゔ') or ('ァ' <= char <= 'ヴ'):
            return True
    return False


def process_excel_col(row: int, col: int, rarity: str, color: str) -> {}:
    row_max = row + 4
    col_max = col + 7
    tmp_name = sheet.cell(row=row, column=col).value
    # print(row, col, tmp_name)
    parts = tmp_name.split("（")
    cel_data = {
        "name": parts[0].strip(),
        "nickname": parts[1].replace("）", "").strip() if len(parts) > 1 else "",
        "稀有度": rarity,
        "破数": sheet.cell(row=row + 2, column=col + 2).value,
        "attributes": [
            {"第一属性": CardCalculator.convert_formula(sheet.cell(row=row + 2, column=col_max - 2).value)},
            {"第二属性": CardCalculator.convert_formula(sheet.cell(row=row + 2, column=col_max - 1).value)},
            {"第三属性": CardCalculator.convert_formula(sheet.cell(row=row + 2, column=col_max).value)}
        ],
        "tags": [
            val for val in (
                sheet.cell(row=row_max, column=col_max - 2).value,
                sheet.cell(row=row + 3, column=col_max - 2).value,
            ) if val is not None],
        "color": color,
        "bonuses": []
    }
    bonus_candidates = [
        {sheet.cell(row=row + 1, column=col + 3).value: sheet.cell(row=row + 2, column=col + 3).value},
        {sheet.cell(row=row + 1, column=col + 4).value: sheet.cell(row=row + 2, column=col + 4).value},
        {sheet.cell(row=row + 3, column=col + 2).value: sheet.cell(row=row_max, column=col + 2).value},
        {sheet.cell(row=row + 3, column=col + 3).value: sheet.cell(row=row_max, column=col + 3).value},
        {sheet.cell(row=row + 3, column=col + 4).value: sheet.cell(row=row_max, column=col + 4).value}
    ]

    for bonus in bonus_candidates:
        if not any(key is None for key in bonus):
            processed_bonus = {key: CardCalculator.convert_formula(value) for key, value in bonus.items()}
            cel_data["bonuses"].append(processed_bonus)
    # 判断是否有道具
    item = sheet.cell(row=row, column=col_max + 1).value
    if item:
        item_row, item_col = row, col_max + 1
        item = {
            item: sheet.cell(row=item_row + 1, column=item_col).value,
            "道具第一属性加成": sheet.cell(row=item_row + 2, column=item_col).value,
            "道具第二属性加成": sheet.cell(row=item_row + 3, column=item_col).value,
            "道具第三属性加成": sheet.cell(row=item_row + 4, column=item_col).value
        }
        cel_data['item'] = {}
        for key, value in item.items():
            if StrUtil.is_str(value) and value.startswith('='):
                cel_data['item'][key] = CardCalculator.convert_formula(value)
            else:
                cel_data['item'][key] = value
    return cel_data


def process_excel():
    colors = ["红", "蓝", "黄"]
    cols = []
    data = []
    for col in range(1, sheet.max_column + 1):
        value = sheet.cell(row=2, column=col).value
        if type(value) is str and contains_japanese(value):
            if col not in cols:  # 避免重复
                cols.append(col)  # 保持插入顺序
    for i in range(0, len(cols)):
        for row in range(1, sheet.max_row + 1):
            col = cols[i]
            value = sheet.cell(row=row, column=col).value
            if type(value) is str and contains_japanese(value):
                color = colors[i % 3]
                rarity = Rarity.SSR.value
                if i > 3:
                    rarity = Rarity.SR.value
                data.append(process_excel_col(row, col, rarity, color))
    s = replace_refs_with_dict(data)
    # 保存结果
    with open('../resource/card/持有情况_数值和公式.json', 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=4)


def replace_refs_with_dict(data: list) -> list:
    # 1. 将data转为JSON字符串
    json_str = json.dumps(data, ensure_ascii=False)
    print("route_data.keys()", route_data.keys())
    # 2. 按键长度降序排序，避免短键误替换长键（如先替换"'路线'!B11"再替换"'路线'!B1"）
    route_sorted_keys = sorted(route_data.keys(), key=len, reverse=True)
    print("entry_data.keys()", entry_data.keys())
    # 2. 按键长度降序排序，避免短键误替换长键（如先替换"'词条'!B11"再替换"'词条'!B1"）
    entry_sorted_keys = sorted(entry_data.keys(), key=len, reverse=True)

    # 3. 逐个替换Excel引用为中文描述
    for excel_ref in route_sorted_keys:
        json_str = json_str.replace(excel_ref.__str__(), route_data[excel_ref.__str__()])
    # 4. 逐个替换Excel引用为中文描述
    for excel_ref in entry_sorted_keys:
        json_str = json_str.replace(excel_ref.__str__(), entry_data[excel_ref.__str__()])

    json_str = json_str.replace("路线!C6", "user['塞卡等效属性(20/1)']")

    json_str = json_str.replace("路线!B4", "user['道具属性']")
    # 5. 替换在持有情况页json和单元格映射
    all_cell_dict = make_all_cell_value_dict()
    all_cell_sorted_keys = sorted(all_cell_dict.keys(), key=len, reverse=True)
    for excel_ref in all_cell_sorted_keys:
        json_str = json_str.replace(excel_ref.__str__(), all_cell_dict[excel_ref.__str__()])

    # 4. 将字符串转回Python对象
    return json.loads(json_str)


def make_all_cell_value_dict() -> dict:
    """建立excel表中，所有单元格和上方名称之间的关系"""
    cell_dict: dict = {}
    for row in range(2, sheet.max_row + 1):
        for col in range(1, sheet.max_column + 1):
            value = sheet.cell(row=row, column=col).value
            name = sheet.cell(row=row - 1, column=col).value
            if StrUtil.is_str(name) and StrUtil.is_not_blank(name):
                if ObjUtil.not_empty(value):
                    key = ExcelUtil.col_row_to_excel_col(col, row)
                    if key=='Z17':
                        print(name,key,value)
                    if StrUtil.is_str(name) and name.startswith('='):
                        cell_dict[key] = name
                    else:
                        cell_dict[key] = f"card['{name}']"

        # 1. 将data转为JSON字符串
    json_str = json.dumps(cell_dict, ensure_ascii=False)
    print("route_data.keys()", route_data.keys())
    # 2. 按键长度降序排序，避免短键误替换长键（如先替换"'路线'!B11"再替换"'路线'!B1"）
    route_sorted_keys = sorted(route_data.keys(), key=len, reverse=True)
    print("entry_data.keys()", entry_data.keys())
    # 2. 按键长度降序排序，避免短键误替换长键（如先替换"'词条'!B11"再替换"'词条'!B1"）
    entry_sorted_keys = sorted(entry_data.keys(), key=len, reverse=True)
    # 3. 逐个替换Excel引用为中文描述
    for excel_ref in route_sorted_keys:
        json_str = json_str.replace(excel_ref.__str__(), route_data[excel_ref.__str__()])
    # 4. 逐个替换Excel引用为中文描述
    for excel_ref in entry_sorted_keys:
        json_str = json_str.replace(excel_ref.__str__(), entry_data[excel_ref.__str__()])
    json_str = json_str.replace("路线!C6", "user['塞卡等效属性(20/1)']")
    json_str = json_str.replace("路线!B4", "user['道具属性']")
    cell_dict = json.loads(json_str)
    # 遍历 cell_dict 中的每个键值对
    # cell_dict = relace_self(cell_dict)
    # 保存为JSON文件
    with open(f'../resource/tmp/cell_dict.json', 'w', encoding='utf-8') as _f:
        json.dump(cell_dict, _f, ensure_ascii=False, indent=4)
    return cell_dict


def relace_self(cell_dict):
    for key,value in cell_dict.items():
        row,col=ExcelUtil.cell_to_row_col(key)
        for j in range(col,1):
            for i in range(row,1):
                ikey=ExcelUtil.col_row_to_excel_col(j,i)
                cell_dict[key]=value.replace(ikey,cell_dict[ikey])
    return cell_dict


if __name__ == '__main__':
    process_excel()
