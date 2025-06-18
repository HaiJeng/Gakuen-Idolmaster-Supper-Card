import json
import re

from common.config import catch_card, attr_name_list
from model.SupportCard import SupportCard
from util.ObjUtil import ObjUtil
from util.StrUtil import StrUtil


class CardCalculator:
    """
    用于根据持有情况.json计算支援卡属性
    使用方式为
    # 加载卡片数据
    with open('../resource/card/持有情况_数值和公式.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    with open('../resource/entry/词条.json', 'r', encoding='utf-8') as f:
        entry = json.load(f)
    with open('../resource/route/路线选择_均衡.json', 'r', encoding='utf-8') as f:
        route = json.load(f)
    with open('../resource/user_config.json', 'r', encoding='utf-8') as f:
        user = json.load(f)

    # 计算第一张卡片
    calculated_card = CardCalculator.calculate_card(
        cards[0],
        route,
        entry,
        user
    )
    """

    @staticmethod
    def AND(*conditions):
        return all(conditions)

    @staticmethod
    def OR(*conditions):
        return any(conditions)

    # 自定义函数映射Excel函数
    @staticmethod
    def IF(condition, true_val, false_val):
        return true_val if condition else false_val

    @staticmethod
    def INT(value):
        return int(value)

    @staticmethod
    def CHOOSE(index, *choices):
        return choices[index - 1] if 1 <= index <= len(choices) else None

    @staticmethod
    def INDEX(arr, index):
        return arr[index - 1] if 1 <= index <= len(arr) else None

    # 转换Excel公式为Python表达式
    @staticmethod
    def convert_formula(formula):
        if not StrUtil.is_str(formula):
            return formula
        # 移除开头的等号
        if formula.startswith('='):
            formula = formula[1:]

        # 处理比较运算符中的等号（如 =, <==, >==）
        # 使用更复杂的正则表达式，确保不匹配字符串中的等号
        def replace_equals(match):
            # 检查等号是否在引号内
            before = match.string[:match.start()]
            quotes_count = before.count('"') + before.count("'")
            if quotes_count % 2 != 0:  # 如果在引号内
                return '='  # 不替换
            return '=='  # 替换为双等号

        formula = re.sub(r'(?<![<>=!])=(?![=])', replace_equals, formula)
        formula = formula.replace('<==', '<=').replace('>==', '>=')

        # 处理嵌套等号（仅移除嵌套公式开头的等号）
        def replace_nested_equal(match):
            sub_formula = match.group(1)
            if sub_formula.startswith('='):
                sub_formula = sub_formula[1:]
            return sub_formula

        # 改进的正则表达式，只匹配函数参数中的等号开头的子公式
        formula = re.sub(r'=(?=\w+\()(.*?)(?=[,)]|$)', replace_nested_equal, formula)

        # 替换Excel函数为Python函数
        replacements = {
            'IF(': 'CardCalculator.IF(',
            'INT(': 'CardCalculator.INT(',
            'CHOOSE(': 'CardCalculator.CHOOSE(',
            'INDEX(': 'CardCalculator.INDEX(',
            'AND(': 'CardCalculator.AND(',
            'OR(': 'CardCalculator.OR(',
        }

        for old, new in replacements.items():
            formula = formula.replace(old, new)

        return formula

    # 计算单个公式
    @staticmethod
    def eval_formula(formula, context):
        try:
            return eval(formula, context)
        except Exception as e:
            print(f"Error evaluating formula: {formula}\nError: {str(e)}")
            # 打印上下文信息，帮助调试
            if 'card' in context:
                print("Card context keys:", list(context['card'].keys()))
            return None

    # 计算整张卡片
    @staticmethod
    def calculate_card(card_data: dict, route_dict, entry_dict, user_dict):
        # 准备卡片数据字典
        card_dict = {
            '破数': card_data['破数'],
            'name': card_data['name']
        }
        for key in catch_card:
            card_dict[key] = user_dict[key]

        # 计算所有bonuses
        for bonus in card_data['bonuses']:
            for key, formula in bonus.items():
                context = {
                    'card': card_dict,
                    'route': route_dict,
                    'entry': entry_dict,
                    'user': user_dict,
                    'CardCalculator': CardCalculator
                }
                card_dict[key] = CardCalculator.eval_formula(formula, context)
        # 计算所有属性
        for attr in card_data['attributes']:
            for key, formula in attr.items():
                context = {
                    'card': card_dict,
                    'route': route_dict,
                    'entry': entry_dict,
                    'user': user_dict,
                    'CardCalculator': CardCalculator
                }
                card_dict[key] = CardCalculator.eval_formula(formula, context)

        if card_data.__contains__('item'):
            if StrUtil.is_str(card_data['item']['道具属性']):
                context = {
                    'card': card_dict,
                    'route': route_dict,
                    'entry': entry_dict,
                    'user': user_dict,
                    'CardCalculator': CardCalculator
                }
                card_dict['道具属性'] = CardCalculator.eval_formula(card_data['item']['道具属性'], context)
            else:
                card_dict['道具属性'] = card_data['item']['道具属性']
            for key, formula in card_data['item'].items():
                if key != '道具属性':
                    context = {
                        'card': card_dict,
                        'route': route_dict,
                        'entry': entry_dict,
                        'user': user_dict,
                        'CardCalculator': CardCalculator
                    }
                    card_dict[key] = CardCalculator.eval_formula(formula, context)
        data = {
            'name': card_data['name'],
            'color': card_data['color'],
            'breakthrough': card_data['破数'],
            'rarity': card_data['稀有度'],
            'nickname': card_data['nickname'],
            'attributes': {k: card_dict[k] for b in card_data['attributes'] for k, v in b.items()},
            'bonuses': {k: card_dict[k] for b in card_data['bonuses'] for k, v in b.items()},
            'item':  {k: card_dict[k] for k, v in card_data['item'].items()} if card_data.__contains__('item') else {},
        }
        return SupportCard(**data), {
            'card': card_dict,
            'route': route_dict,
            'entry': entry_dict,
            'user': user_dict,
            'CardCalculator': CardCalculator
        }


def calculator_attr(name, context, _attr):
    with open(f'../resource/attr/{_attr}.json', 'r', encoding='utf-8') as _f:
        datas = json.load(_f)
    result = {}
    data = datas[name]
    for key, value in data.items():
        if key != '带出道具或S卡' and ObjUtil.not_empty(value) and StrUtil.is_str(value) and StrUtil.is_not_blank(
                value):
            result[key] = CardCalculator.eval_formula(value, context)
        else:
            result[key] = value
    context.update({'attr': result})
    _calculator_attr = data['calculator_attr']
    for key, value in _calculator_attr.items():
        if ObjUtil.not_empty(value) and StrUtil.is_str(value) and StrUtil.is_not_blank(
                value):
            result[key] = CardCalculator.eval_formula(value, context)
        else:
            result[key] = value
    result.pop('calculator_attr')
    return result


# 使用示例
if __name__ == "__main__":
    # 加载卡片数据
    with open('../resource/card/持有情况_数值和公式.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    with open('../resource/entry/词条.json', 'r', encoding='utf-8') as f:
        entry = json.load(f)
    with open('../resource/route/路线选择_均衡.json', 'r', encoding='utf-8') as f:
        route = json.load(f)
    with open('../resource/user_config.json', 'r', encoding='utf-8') as f:
        user = json.load(f)

    # calculated_card, calculated_dict = CardCalculator.calculate_card(
    #     cards[0],
    #     route,
    #     entry,
    #     user
    # )
    # print(calculated_card, calculator_attr(f"{calculated_card.name}（{calculated_card.nickname}）", calculated_dict))
    # 计算第一张卡片
    for card in cards:
        if card['name']=='ばたんきゅー':
            calculated_card, calculated_dict = CardCalculator.calculate_card(
                card,
                route,
                entry,
                user
            )
            calculated_card.first_attribute= calculator_attr(f"{calculated_card.name}（{calculated_card.nickname}）",
                                calculated_dict,
                                attr_name_list[0])
            calculated_card.second_attribute= calculator_attr(f"{calculated_card.name}（{calculated_card.nickname}）",
                                calculated_dict,
                                attr_name_list[1])
            calculated_card.third_attribute= calculator_attr(f"{calculated_card.name}（{calculated_card.nickname}）",
                                calculated_dict,
                                attr_name_list[2])
            print(calculated_card)
