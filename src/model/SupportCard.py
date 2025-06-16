# models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List


class Rarity(Enum):
    SSR = "SSR"
    SR = "SR"


class Color(Enum):
    RED = "红"
    YELLOW = "黄"
    BLUE = "蓝"


@dataclass
class SupportCard:
    name: str  # 原名
    nickname: str  # 昵称
    rarity: Rarity  # "SSR" / "SR"
    color: Color
    sp: int = 0  # 破数
    attributes: Dict[str, int] = field(default_factory=dict)  # {"first": 100, "second": 80, "third": 60}
    tags: List[str] = field(default_factory=list)  # ["道具", "流派", "强化"] 等
    bonuses: Dict[str, float] = field(default_factory=dict)  # {"基础值": 48, "百分比": 6.5}
    item: Dict[str, float] = None

    def __post_init__(self):
        # 如果传入的是字符串，自动转换为 Enum
        if isinstance(self.rarity, str):
            try:
                self.rarity = Rarity(self.rarity)
            except ValueError:
                raise ValueError(f"Invalid rarity: {self.rarity}. Must be 'SSR' or 'SR'.")
        # 如果传入的是字符串，自动转换为 Enum
        if isinstance(self.color, str):
            try:
                self.color = Color(self.color)
            except ValueError:
                raise ValueError(f"Invalid rarity: {self.color}. Must be 'SSR' or 'SR'.")
