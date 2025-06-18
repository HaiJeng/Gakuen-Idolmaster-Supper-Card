import ast

from util.ObjUtil import ObjUtil


class StrUtil:
    """字符串处理工具类"""

    @staticmethod
    def is_str(obj) -> bool:
        if ObjUtil.is_empty(obj):
            return False
        """检查对象是否为字符串类型"""
        return isinstance(obj, str)

    @staticmethod
    def is_not_blank(string: str) -> bool:
        """
        检查字符串是否非空（非None、非空字符串、非纯空白字符）

        参数:
            string: 要检查的字符串

        异常:
            TypeError: 如果输入不是字符串类型
        """
        if not isinstance(string, str):
            raise TypeError(f"输入必须是字符串类型，实际类型为 {type(string).__name__}")
        return bool(string and not string.isspace())

    @staticmethod
    def contains_japanese(text):
        # 平假名范围: U+3040 - U+309F
        # 片假名范围: U+30A0 - U+30FF
        if text == '':
            return False
        for char in text:
            if ('ぁ' <= char <= 'ゔ') or ('ァ' <= char <= 'ヴ'):
                return True
        return False

    @staticmethod
    def is_blank(string: str) -> bool:
        """
        检查字符串是否为空（None、空字符串或纯空白字符）

        参数:
            string: 要检查的字符串

        异常:
            TypeError: 如果输入不是字符串类型
        """
        if not isinstance(string, str):
            raise TypeError(f"输入必须是字符串类型，实际类型为 {type(string).__name__}")
        return not bool(string and not string.isspace())

    @staticmethod
    def contains_japanese(text: str) -> bool:
        """检查字符串是否包含日文字符"""
        return any('\u3040' <= char <= '\u30ff' or '\u4e00' <= char <= '\u9fff' for char in text)

    @staticmethod
    def safe_trim(text: str, max_len: int = 100, suffix: str = "...") -> str:
        """
        安全截断字符串并添加后缀

        参数:
            text: 要截断的文本
            max_len: 最大长度（包含后缀）
            suffix: 截断后添加的后缀

        返回:
            截断后的字符串
        """
        if not text or len(text) <= max_len:
            return text

        # 确保后缀不会使字符串超过最大长度
        suffix_len = len(suffix)
        if suffix_len >= max_len:
            return suffix[:max_len]

        return text[:max_len - suffix_len] + suffix

    @staticmethod
    def to_camel_case(snake_str: str) -> str:
        """将蛇形命名转换为驼峰命名（例如：my_variable -> myVariable）"""
        if not snake_str:
            return snake_str

        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def to_snake_case(camel_str: str) -> str:
        """将驼峰命名转换为蛇形命名（例如：myVariable -> my_variable）"""
        if not camel_str:
            return camel_str

        result = [camel_str[0].lower()]
        for char in camel_str[1:]:
            if char.isupper():
                result.extend(['_', char.lower()])
            else:
                result.append(char)
        return ''.join(result)

    @staticmethod
    def extract_numbers(text: str) -> list:
        """从字符串中提取所有数字"""
        import re
        return [int(num) for num in re.findall(r'\d+', text)]

    @staticmethod
    def count_substring(text: str, substring: str, case_sensitive: bool = True) -> int:
        """
        计算子字符串出现的次数

        参数:
            text: 主字符串
            substring: 要计数的子字符串
            case_sensitive: 是否区分大小写

        返回:
            出现次数
        """
        if not text or not substring:
            return 0

        if not case_sensitive:
            text = text.lower()
            substring = substring.lower()

        count = start = 0
        while True:
            start = text.find(substring, start) + 1
            if start > 0:
                count += 1
            else:
                return count

    @staticmethod
    def has_uppercase_value(dictionary):
        """
        判断{str,str}的字典中，value是否包含大写，
        :param dictionary: {str,str}
        :return: 包含True/不包含False
        """
        return any(any(char.isupper() for char in value) for value in dictionary.values())

    @staticmethod
    def contains_excel_cell(s: str):
        import re
        # 匹配完整的单元格引用（前后无字母/数字）
        pattern = r'(?:^|[^\w$])(\$?[A-Z]{1,3}\$?\d+)(?:$|[^\w$])'
        return bool(re.search(pattern, s))
    @staticmethod
    def is_safe_expression(source):
        if not StrUtil.is_str(source):
            return False
        try:
            # 尝试解析源代码
            ast.parse(source, mode='eval')
            return True
        except SyntaxError:
            return False