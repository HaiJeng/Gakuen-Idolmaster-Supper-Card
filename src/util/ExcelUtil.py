class ExcelUtil:
    @staticmethod
    def col_row_to_excel_col(num: int, row: int):
        """
        将Excel列索引(整数)和行索引转换为字母单元格
        :param row: 行索引
        :param num: 列索引（从1开始）
        :return: 字母单元格标字符串
        """
        if num < 1:
            raise ValueError("列索引必须为正整数")

        result = []
        while num > 0:
            num -= 1  # 关键步骤：将1-26映射到0-25
            remainder = num % 26  # 计算当前位的字母索引
            result.append(chr(65 + remainder))  # 65是'A'的ASCII码
            num //= 26  # 更新为更高位

        # 将结果反转（因为计算是从低位到高位）
        return ''.join(reversed(result)) + row.__str__()
