import json

from util.ExcelUtil import ExcelUtil
from util.ObjUtil import ObjUtil


class ParseToFirstAttrDictUtil:
    def __init__(self, sheet, sheet_name: str):
        self.sheet = sheet
        self.sheet_name = sheet_name

    def parse_to_first_attr_dict_util(self):
        row_max = 2
        for row in range(2, self.sheet.max_row):
            if ObjUtil.is_empty(self.sheet.cell(row=row, column=1).value):
                row_max = row - 1
                break
        first_attr_dict = {}
        for column in range(4, self.sheet.max_column):
            value = self.sheet.cell(row=1, column=column).value
            if ObjUtil.not_empty(value):
                for row in range(row_max, 1, -1):
                    first_attr_dict.update({
                        ExcelUtil.row_col_to_excel_col(row, column): f"attr['{value}']"
                    })
        with open(f'../resource/tmp/{self.sheet_name}_dict.json', 'w', encoding='utf-8') as f:
            json.dump(first_attr_dict, f, ensure_ascii=False, indent=4)
        return first_attr_dict
