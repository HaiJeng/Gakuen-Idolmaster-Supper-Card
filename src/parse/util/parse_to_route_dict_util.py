import json


class ParseToRouteDictUtil:
    def __init__(self, sheet):
        self.sheet = sheet

    def parse_to_route_dict(self):
        # 查找route单元格的位置
        route_choice_row = None

        for row in range(1, self.sheet.max_row + 1):
            cell_value = self.sheet.cell(row=row, column=2).value
            if cell_value == '路线选择':
                route_choice_row = row
                break
        route_dict = {}
        for row in range(route_choice_row + 1, self.sheet.max_row + 1):
            value = self.sheet.cell(row=row, column=1).value
            print(value)
            if not value:
                break
            route_dict.update({'\'路线\'!B' + str(row): f"route['{value}']"})
            route_dict.update({'路线!B' + str(row): f"route['{value}']"})
        route_dict.update({"路线!C6": "user['塞卡等效属性(20/1)']"})

        route_dict.update({"路线!B4": "user['道具属性']"})
        print(route_dict)
        # 保存为JSON文件
        with open(f'../resource/tmp/route_dict.json', 'w', encoding='utf-8') as f:
            json.dump(route_dict, f, ensure_ascii=False, indent=4)
