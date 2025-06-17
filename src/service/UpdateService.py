import json


def update_card_breakthrough_by_name(breakthrough: int, name: str):
    with open('../resource/card/持有情况_数值和公式.json', 'r', encoding='utf-8') as f:
        cards = json.load(f)
    for card in cards:
        card['name'] = name
        if card['name'] == name:
            card['破数'] = breakthrough
            break
    with open('../resource/card/持有情况_数值和公式.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, ensure_ascii=False, indent=4)


def update_user_config(dict_data: dict):
    with open('../resource/user_config.json', 'r', encoding='utf-8') as f:
        user_config = json.load(f)
    for key, value in dict_data.items():
        if key in user_config:
            user_config[key] = value
    with open('../resource/user_config.json', 'w', encoding='utf-8') as f:
        json.dump(user_config, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    update_card_breakthrough_by_name(-1, 'あら、奇遇ね')
    update_user_config({
        "全力抓卡": 0,
        "干劲抓卡": 0,
        "好调抓卡": 0,
        "好印象抓卡": 0,
        "集中抓卡": 0,
        "强气抓卡": 10,
        "元气抓卡": 0
    })
