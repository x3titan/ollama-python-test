from __future__ import annotations

from typing import Any
from urllib.parse import urljoin
from dataclasses import dataclass, field
import random

class TamPub:
    @staticmethod
    def random_string(options: dict[str, float]) -> str:
        """
        根据权重随机返回一个字符串。

        Args:
            options: 字符串及其对应权重，例如：
                    {"apple": 3.5, "banana": 100, "orange": 20}

        Returns:
            按照权重随机选中的字符串。
        """
        if not options:
            raise ValueError("options不能为空")

        if any(weight < 0 for weight in options.values()):
            raise ValueError("权重不能是负数")

        if sum(options.values()) <= 0:
            raise ValueError("至少需要一个大于0的权重")

        strings = list(options.keys())
        weights = list(options.values())

        return random.choices(strings, weights=weights, k=1)[0]


