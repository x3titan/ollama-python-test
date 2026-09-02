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

    @staticmethod
    def random_linear_int(a: int, b: int, a_weight: float, b_weight: float) -> int:
        """
        根据线性变化的权重，随机产生a到b之间的整数（包含a和b）。

        Args:
            a: 最小整数。
            b: 最大整数。
            a_weight: 整数a对应的权重。
            b_weight: 整数b对应的权重。

        Returns:
            按照线性权重随机选中的整数。
        """
        if a > b:
            raise ValueError("a不能大于b")

        if a_weight < 0 or b_weight < 0:
            raise ValueError("权重不能是负数")

        if a == b:
            return a

        if a_weight == 0 and b_weight == 0:
            raise ValueError("a_weight和b_weight不能同时为0")

        numbers = list(range(a, b + 1))

        weights = [a_weight + (b_weight - a_weight) * (number - a) / (b - a) for number in numbers]

        return random.choices(numbers, weights=weights, k=1)[0]


    @staticmethod
    def random_hyperbolic_int(a: int, b: int, a_weight: float, b_weight: float, curve_strength: float = 4.0) -> int:
        """
        按照双曲线型权重，随机产生a到b之间的整数（包含a和b）。

        Args:
            a: 最小整数。
            b: 最大整数。
            a_weight: 整数a对应的权重。
            b_weight: 整数b对应的权重。
            curve_strength: 曲线凹陷程度。
                            0表示直线；
                            数值越大，曲线弯曲越明显。

        Returns:
            按照双曲线型权重随机选中的整数。
        """
        if a > b:
            raise ValueError("a不能大于b")

        if a_weight < 0 or b_weight < 0:
            raise ValueError("权重不能是负数")

        if a_weight == 0 and b_weight == 0:
            raise ValueError("两个权重不能同时为0")

        if curve_strength < 0:
            raise ValueError("curve_strength不能是负数")

        if a == b:
            return a

        numbers = list(range(a, b + 1))
        weights = []

        for number in numbers:
            # 将当前位置转换为0～1
            position = (number - a) / (b - a)

            # 双曲线型变化：从1下降到0
            curve_value = (1 - position) / (1 + curve_strength * position)

            weight = b_weight + (a_weight - b_weight) * curve_value

            weights.append(weight)

        return random.choices(numbers, weights=weights, k=1)[0]
