from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EDataSet:
    """
    用于存储二维字符串数据。

    数据访问顺序与原 JavaScript 保持一致：
        set_data(col_index, row_index, value)
        get_data(col_index, row_index)
    """

    col_count: int = 0
    row_count: int = 0
    _data: list[list[str]] = field(default_factory=list)

    def set_col_count(self, col_count: int) -> None:
        if col_count < 0:
            raise ValueError("列数不能小于 0")

        self.col_count = col_count
        self._resize()

    def set_row_count(self, row_count: int) -> None:
        if row_count < 0:
            raise ValueError("行数不能小于 0")

        self.row_count = row_count
        self._resize()

    def _resize(self) -> None:
        old_data = self._data

        self._data = [
            ["" for _ in range(self.col_count)]
            for _ in range(self.row_count)
        ]

        old_row_count = len(old_data)
        old_col_count = len(old_data[0]) if old_data else 0

        copy_rows = min(old_row_count, self.row_count)
        copy_cols = min(old_col_count, self.col_count)

        for row_index in range(copy_rows):
            for col_index in range(copy_cols):
                self._data[row_index][col_index] = old_data[row_index][col_index]

    def set_data(
        self,
        col_index: int,
        row_index: int,
        value: Optional[str],
    ) -> None:
        self._check_position(col_index, row_index)
        self._data[row_index][col_index] = "" if value is None else str(value)

    def get_data(self, col_index: int, row_index: int) -> str:
        self._check_position(col_index, row_index)
        return self._data[row_index][col_index]

    def _check_position(self, col_index: int, row_index: int) -> None:
        if not 0 <= col_index < self.col_count:
            raise IndexError(f"列索引超出范围：{col_index}")

        if not 0 <= row_index < self.row_count:
            raise IndexError(f"行索引超出范围：{row_index}")

    def to_rows(self) -> list[list[str]]:
        """返回按行排列的数据副本。"""
        return [row.copy() for row in self._data]


class EIO:
    """
    前后台数据流打包与解包工具。

    buffi:
        输入缓存，即需要读取的数据字符串。

    buffo:
        输出缓存，即已经打包完成的数据字符串。

    sp:
        当前输入缓存的读取位置。
    """

    def __init__(self, input_buffer: str = "") -> None:
        self.buffi = input_buffer
        self.buffo = ""
        self.sp = 0

    def clear(self) -> None:
        """清空输入缓存、输出缓存和读取指针。"""
        self.buffi = ""
        self.buffo = ""
        self.sp = 0

    def clear_output(self) -> None:
        """只清空输出缓存。"""
        self.buffo = ""

    def set_input(self, data: Optional[str]) -> None:
        """设置输入缓存，并将读取指针归零。"""
        self.buffi = "" if data is None else str(data)
        self.sp = 0

    def get_output(self) -> str:
        """取得已经打包完成的输出数据。"""
        return self.buffo

    def remaining_length(self) -> int:
        """取得输入缓存中尚未读取的字符数量。"""
        return max(0, len(self.buffi) - self.sp)

    def append_byte(self, value: int) -> None:
        """
        写入一个无符号 8 位整数。

        输出占两个十六进制字符，例如：
            0   -> "00"
            15  -> "0f"
            255 -> "ff"
        """
        value &= 0xFF
        self.buffo += f"{value:02x}"

    def append_word(self, word: int) -> None:
        """
        以小端序写入一个无符号 16 位整数。

        例如：
            0x1234 -> "3412"
        """
        word &= 0xFFFF

        self.append_byte(word & 0xFF)
        self.append_byte(word >> 8)

    def append_int32(self, int32: int) -> None:
        """
        以小端序写入一个无符号 32 位整数。

        例如：
            0x12345678 -> "78563412"
        """
        int32 &= 0xFFFFFFFF

        self.append_word(int32 & 0xFFFF)
        self.append_word(int32 >> 16)

    def append_string8(self, value: Optional[str]) -> None:
        """
        写入最长 255 个字符的字符串。

        格式：
            1 字节长度 + 字符串正文
        """
        text = "" if value is None else str(value)
        text = text[:0xFF]

        self.append_byte(len(text))
        self.buffo += text

    def append_string16(self, value: Optional[str]) -> None:
        """
        写入最长 65535 个字符的字符串。

        格式：
            2 字节长度 + 字符串正文
        """
        text = "" if value is None else str(value)
        text = text[:0xFFFF]

        self.append_word(len(text))
        self.buffo += text

    def append_string32(self, value: Optional[str]) -> None:
        """
        写入一个使用 32 位长度字段的字符串。

        格式：
            4 字节长度 + 字符串正文
        """
        text = "" if value is None else str(value)

        if len(text) > 0xFFFFFFFF:
            raise ValueError("字符串长度超过 32 位无符号整数的表示范围")

        self.append_int32(len(text))
        self.buffo += text

    def read_byte(self) -> int:
        """
        读取一个无符号 8 位整数。

        输入缓存中的两个十六进制字符表示一个字节。
        """
        if self.sp + 2 > len(self.buffi):
            self.sp = len(self.buffi)
            return 0

        text = self.buffi[self.sp:self.sp + 2]
        self.sp += 2

        try:
            return int(text, 16)
        except ValueError as exc:
            raise ValueError(
                f"位置 {self.sp - 2} 的内容不是有效十六进制字节：{text!r}"
            ) from exc

    def read_word(self) -> int:
        """以小端序读取一个无符号 16 位整数。"""
        low_byte = self.read_byte()
        high_byte = self.read_byte()

        return low_byte | (high_byte << 8)

    def read_int32(self) -> int:
        """以小端序读取一个无符号 32 位整数。"""
        low_word = self.read_word()
        high_word = self.read_word()

        return low_word | (high_word << 16)

    def read_string8(self) -> str:
        """读取一个使用 8 位长度字段的字符串。"""
        length = self.read_byte()
        return self._read_string_body(length)

    def read_string16(self) -> str:
        """读取一个使用 16 位长度字段的字符串。"""
        length = self.read_word()
        return self._read_string_body(length)

    def read_string32(self) -> str:
        """读取一个使用 32 位长度字段的字符串。"""
        length = self.read_int32()
        return self._read_string_body(length)

    def _read_string_body(self, length: int) -> str:
        available_length = len(self.buffi) - self.sp
        actual_length = min(available_length, max(0, length))

        result = self.buffi[self.sp:self.sp + actual_length]
        self.sp += actual_length

        return result

    def append_data_set(self, data_set: EDataSet) -> None:
        """
        写入一个 EDataSet。

        格式：
            Word：列数
            Word：行数
            String16：每个单元格的数据
        """
        self.append_word(data_set.col_count)
        self.append_word(data_set.row_count)

        for row_index in range(data_set.row_count):
            for col_index in range(data_set.col_count):
                self.append_string16(
                    data_set.get_data(col_index, row_index)
                )

    def read_data_set(self) -> EDataSet:
        """读取一个 EDataSet。"""
        result = EDataSet()

        result.set_col_count(self.read_word())
        result.set_row_count(self.read_word())

        for row_index in range(result.row_count):
            for col_index in range(result.col_count):
                result.set_data(
                    col_index,
                    row_index,
                    self.read_string16(),
                )

        return result