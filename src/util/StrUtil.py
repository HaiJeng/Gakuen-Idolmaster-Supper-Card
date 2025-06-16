class StrUtil:
    """字符串处理工具类"""

    @staticmethod
    def is_str(obj) -> bool:
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
    def remove_special_chars(text: str, keep_chars: str = "") -> str:
        """
        移除特殊字符，只保留字母、数字和指定字符

        参数:
            text: 要处理的文本
            keep_chars: 额外保留的字符

        返回:
            处理后的字符串
        """
        import re
        pattern = f"[^a-zA-Z0-9\s{re.escape(keep_chars)}]"
        return re.sub(pattern, '', text)

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