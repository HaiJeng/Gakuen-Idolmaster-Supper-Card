import json

from common.config import catch_card
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
        # 移除开头的等号
        if formula.startswith('='):
            formula = formula[1:]

        # 替换Excel函数为Python函数
        replacements = {
            'IF(': 'CardCalculator.IF(',
            'INT(': 'CardCalculator.INT(',
            'CHOOSE(': 'CardCalculator.CHOOSE(',
            'INDEX(': 'CardCalculator.INDEX(',
            '=': '==',  # 新增：将 = 替换为 ==
            '<==': '<=',
            '>==': '>='
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
    def calculate_card(card_data:dict, route_dict, entry_dict, user_dict):
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
        attributes = {}
        for attr in card_data['attributes']:
            for key, formula in attr.items():
                context = {
                    'card': card_dict,
                    'route': route_dict,
                    'entry': entry_dict,
                    'user': user_dict,
                    'CardCalculator': CardCalculator
                }
                attributes[key] = CardCalculator.eval_formula(formula, context)
                card_dict[key] = attributes[key]
        item = {}

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
                    item[key] = CardCalculator.eval_formula(formula, context)
            item['道具属性'] = card_dict['道具属性']

        data = {
            'name': card_data['name'],
            'color': card_data['color'],
            'sp': card_data['破数'],
            'rarity': card_data['稀有度'],
            'nickname': card_data['nickname'],
            'attributes': attributes,
            'bonuses': {k: card_dict[k] for b in card_data['bonuses'] for k, v in b.items()},
            'item': item
        }
        return SupportCard(**data)


# 使用示例
if __name__ == "__main__":
    # 加载卡片数据
    with open('../resource/card/持有情况_数值和公式.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    # with open('test.json', 'r', encoding='utf-8') as f:
    #     cards = json.load(f)
    with open('../resource/entry/词条.json', 'r', encoding='utf-8') as f:
        entry = json.load(f)
    with open('../resource/route/路线选择_均衡.json', 'r', encoding='utf-8') as f:
        route = json.load(f)
    with open('../resource/user_config.json', 'r', encoding='utf-8') as f:
        user = json.load(f)

    # 计算第一张卡片
    for card in cards:
        calculated_card = CardCalculator.calculate_card(
            card,
            route,
            entry,
            user
        )
        print(calculated_card)
