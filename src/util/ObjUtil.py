class ObjUtil:
    """通用对象操作工具类"""

    @staticmethod
    def deep_merge(dict1: dict, dict2: dict) -> dict:
        """
        深度合并两个字典（递归合并嵌套字典）

        参数:
            dict1: 基础字典
            dict2: 要合并的字典

        返回:
            合并后的新字典
        """
        if not isinstance(dict1, dict) or not isinstance(dict2, dict):
            return dict2

        merged = dict1.copy()
        for key, value in dict2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = ObjUtil.deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged

    @staticmethod
    def get_nested_value(obj, path: str, default=None, separator='.'):
        """
        获取嵌套对象中的值

        参数:
            obj: 要查询的对象（字典、列表或对象）
            path: 属性路径（如 'user.address.city'）
            default: 找不到时的默认值
            separator: 路径分隔符

        返回:
            找到的值或默认值
        """
        keys = path.split(separator)
        current = obj

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif isinstance(current, list) and key.isdigit():
                index = int(key)
                if 0 <= index < len(current):
                    current = current[index]
                else:
                    return default
            elif hasattr(current, key):
                current = getattr(current, key)
            else:
                return default

        return current

    @staticmethod
    def set_nested_value(obj, path: str, value, separator='.'):
        """
        设置嵌套对象中的值

        参数:
            obj: 要修改的对象（字典）
            path: 属性路径（如 'user.address.city'）
            value: 要设置的值
            separator: 路径分隔符
        """
        keys = path.split(separator)
        current = obj

        for i, key in enumerate(keys[:-1]):
            if key not in current:
                # 创建缺失的嵌套字典
                current[key] = {}
            current = current[key]

            # 如果路径部分不是字典，则覆盖为字典
            if not isinstance(current, dict):
                current = {}

        current[keys[-1]] = value

    @staticmethod
    def is_empty(obj) -> bool:
        """
        检查对象是否为空（None、空容器、空字符串等）

        参数:
            obj: 要检查的对象

        返回:
            是否为空
        """
        if obj is None:
            return True
        if isinstance(obj, (str, list, tuple, set, dict)):
            return len(obj) == 0
        if hasattr(obj, '__len__'):
            return len(obj) == 0
        return False
    @staticmethod
    def not_empty(obj) -> bool:
        """
        检查对象是否为空（None、空容器、空字符串等）

        参数:
            obj: 要检查的对象

        返回:
            是否为空
        """
        return not ObjUtil.is_empty(obj)

    @staticmethod
    def to_dict(obj, exclude_none=False, exclude_empty=False):
        """
        将对象转换为字典（支持嵌套对象）

        参数:
            obj: 要转换的对象
            exclude_none: 是否排除值为None的属性
            exclude_empty: 是否排除空值（空列表、空字典等）

        返回:
            转换后的字典
        """
        if isinstance(obj, dict):
            return {k: ObjUtil.to_dict(v, exclude_none, exclude_empty) for k, v in obj.items()
                    if not (exclude_none and v is None) and not (exclude_empty and ObjUtil.is_empty(v))}

        if isinstance(obj, list):
            return [ObjUtil.to_dict(item, exclude_none, exclude_empty) for item in obj]

        if isinstance(obj, tuple):
            return tuple(ObjUtil.to_dict(item, exclude_none, exclude_empty) for item in obj)

        if hasattr(obj, '__dict__'):
            return ObjUtil.to_dict(obj.__dict__, exclude_none, exclude_empty)

        return obj

    @staticmethod
    def filter_dict(obj: dict, keys_to_keep=None, keys_to_remove=None):
        """
        过滤字典，保留或删除指定键

        参数:
            obj: 要过滤的字典
            keys_to_keep: 要保留的键列表（优先使用）
            keys_to_remove: 要删除的键列表

        返回:
            过滤后的新字典
        """
        if keys_to_keep is not None:
            return {k: v for k, v in obj.items() if k in keys_to_keep}

        if keys_to_remove is not None:
            return {k: v for k, v in obj.items() if k not in keys_to_remove}

        return obj.copy()

    @staticmethod
    def clone(obj, deep=True):
        """
        克隆对象（支持浅克隆和深克隆）

        参数:
            obj: 要克隆的对象
            deep: 是否深度克隆

        返回:
            克隆后的对象
        """
        import copy
        return copy.deepcopy(obj) if deep else copy.copy(obj)

    @staticmethod
    def flatten_dict(d: dict, parent_key='', separator='.'):
        """
        展平嵌套字典

        参数:
            d: 要展平的字典
            parent_key: 父键前缀（内部使用）
            separator: 键分隔符

        返回:
            展平后的字典
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(ObjUtil.flatten_dict(v, new_key, separator=separator).items())
            else:
                items.append((new_key, v))
        return dict(items)

    @staticmethod
    def unflatten_dict(d: dict, separator='.'):
        """
        将展平的字典还原为嵌套字典

        参数:
            d: 展平的字典
            separator: 键分隔符

        返回:
            嵌套字典
        """
        result = {}
        for key, value in d.items():
            parts = key.split(separator)
            current = result
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        return result

    @staticmethod
    def compare(obj1, obj2) -> bool:
        """
        深度比较两个对象是否相等（支持嵌套结构）

        参数:
            obj1: 第一个对象
            obj2: 第二个对象

        返回:
            是否相等
        """
        import json
        return json.dumps(obj1, sort_keys=True) == json.dumps(obj2, sort_keys=True)

    @staticmethod
    def find_in_list(lst: list, condition: callable):
        """
        在列表中查找满足条件的第一个元素

        参数:
            lst: 要搜索的列表
            condition: 条件函数（返回bool）

        返回:
            找到的元素或None
        """
        return next((item for item in lst if condition(item)), None)

    @staticmethod
    def safe_get(obj, *keys, default=None):
        """
        安全获取对象的属性或字典的值（避免KeyError/AttributeError）

        参数:
            obj: 要查询的对象
            keys: 键序列（属性名或字典键）
            default: 找不到时的默认值

        返回:
            找到的值或默认值
        """
        current = obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            elif hasattr(current, key):
                current = getattr(current, key)
            else:
                return default
        return current