from openpyxl.utils import column_index_from_string


class ExcelUtil:
    @staticmethod
    def col_row_to_excel_col(col: int, row: int):
        """
        将Excel列索引(整数)和行索引转换为字母单元格
        :param row: 行索引
        :param col: 列索引（从1开始）
        :return: 字母单元格标字符串
        """
        if col < 1:
            raise ValueError("列索引必须为正整数")

        result = []
        while col > 0:
            col -= 1  # 关键步骤：将1-26映射到0-25
            remainder = col % 26  # 计算当前位的字母索引
            result.append(chr(65 + remainder))  # 65是'A'的ASCII码
            col //= 26  # 更新为更高位

        # 将结果反转（因为计算是从低位到高位）
        return ''.join(reversed(result)) + row.__str__()
    @staticmethod
    def cell_to_row_col(cell: str) -> tuple[int, int]:
        # 分离列字母和行号
        col_str = ''.join(filter(str.isalpha, cell)).upper()
        row_str = ''.join(filter(str.isdigit, cell))

        # 转换列字母为列号
        col = column_index_from_string(col_str)
        row = int(row_str)

        return row, col
