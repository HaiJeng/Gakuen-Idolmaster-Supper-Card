import json

from util.ExcelUtil import ExcelUtil
from util.ObjUtil import ObjUtil


class ParseToEntryDictUtil:
    def __init__(self, sheet):
        self.sheet = sheet

    def parse_to_route_dict(self):
        route_dict = {}
        for row in range(2, self.sheet.max_row + 1):
            cell_value = self.sheet.cell(row=row, column=1).value
            if ObjUtil.is_empty(cell_value):
                break
            if cell_value == '删卡':
                for col in range(3, 3 + 2):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SSR']['{cell_value}'][{col - 3}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
                for col in range(3 + 3, 3 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SSR']['次限{cell_value}'][{col - 3 - 3}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
            elif cell_value == '百分比' or cell_value == '基础值':
                for col in range(3, 3 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SSR']['{cell_value}'][{col - 3}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
                for col_left in range(3, 3 + 5):
                    for col_right in range(col_left + 1, 3 + 5):
                        name1 = ExcelUtil.row_col_to_excel_col(row, col_left)
                        name2 = ExcelUtil.row_col_to_excel_col(row, col_right)
                        value = f"entry['SSR']['{cell_value}'][{col_left - 3}:{col_right - 3 + 1}]"
                        route_dict.update({f"词条!{name1}:{name2}": f"{value}"})
                        route_dict.update({f"'词条'!{name1}:{name2}": f"{value}"})
            else:
                for col in range(3, 3 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SSR']['{cell_value}'][{col - 3}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
        for row in range(2, self.sheet.max_row + 1):
            cell_value = self.sheet.cell(row=row, column=1).value
            if ObjUtil.is_empty(cell_value):
                break
            if cell_value == '删卡':
                for col in range(9, 9 + 2):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SR']['{cell_value}'][{col - 9}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
                for col in range(9 + 3, 9 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SR']['次限{cell_value}'][{col - 9 - 3}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
            elif cell_value == '百分比' or cell_value == '基础值':
                for col in range(9, 9 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SR']['{cell_value}'][{col - 9}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
                for col_left in range(9, 9 + 5):
                    for col_right in range(col_left + 1, 9 + 5):
                        name1 = ExcelUtil.row_col_to_excel_col(row, col_left)
                        name2 = ExcelUtil.row_col_to_excel_col(row, col_right)
                        value = f"entry['SR']['{cell_value}'][{col_left - 9}:{col_right - 9 + 1}]"
                        route_dict.update({f"词条!{name1}:{name2}": f"{value}"})
                        route_dict.update({f"'词条'!{name1}:{name2}": f"{value}"})
            else:
                for col in range(9, 9 + 5):
                    name = ExcelUtil.row_col_to_excel_col(row, col)
                    value = f"entry['SR']['{cell_value}'][{col - 9}]"
                    route_dict.update({f"词条!{name}": value})
                    route_dict.update({f"'词条'!{name}": value})
        # 保存为JSON文件
        with open(f'../resource/tmp/entry_dict.json', 'w', encoding='utf-8') as f:
            json.dump(route_dict, f, ensure_ascii=False, indent=4)
