"""Упрощённый аналог `PyLong` из CPython: целое произвольной точности.

Как в CPython (``Objects/longobject.c``): число хранится в виде массива
"цифр" (limbs) в системе счисления по основанию ``BASE = 2 ** SHIFT``,
little-endian. Знак хранится отдельно (в CPython — в ``lv_tag``).

    value = sign * sum(digits[i] * BASE**i for i in range(len(digits)))

Инварианты представления:
- ``0 <= digits[i] <= MASK`` для всех ``i``;
- ``digits[-1] != 0`` для ненулевых чисел (нормализованность);
- ``sign``: 0 — ноль, 1 — положительное, -1 — отрицательное.

Задание (см. README.md): реализуйте ``BigInt.from_string``,
``BigInt.to_string`` и функции ``neg``, ``add``, ``sub``, ``mul``, ``compare``.
Каркас ниже менять не нужно — тесты и представление завязаны на него.
"""

from __future__ import annotations

SHIFT = 30          # PyLong_SHIFT в CPython
BASE = 1 << SHIFT   # 2 ** 30
MASK = BASE - 1     # PyLong_MASK

Digits = list[int]


class BigInt:
    """Целое произвольной точности."""

    __slots__ = ("digits", "sign")

    def __init__(self, digits: Digits, sign: int) -> None:
        self.digits = digits
        self.sign = sign

    # --- каркас: предоставлен, не переделывать ----------------------------

    @classmethod
    def _normalize(cls, digits: Digits, sign: int) -> BigInt:
        """Отбрасывает старшие нулевые разряды и обнуляет знак у нуля.

        ``sign == 0`` для ненулевого значения трактуется как «авто»:
        число положительное.
        """
        while len(digits) > 1 and digits[-1] == 0:
            digits.pop()
        if len(digits) == 1 and digits[0] == 0:
            return cls([0], 0)
        if sign == 0:
            sign = 1
        return cls(digits, sign)

    @classmethod
    def from_int(cls, value: int) -> BigInt:
        """Строит BigInt из встроенного int (для тестов и удобства)."""
        if not isinstance(value, int):
            raise TypeError(f"ожидался int, получено: {type(value).__name__}")
        sign = (value > 0) - (value < 0)
        value = abs(value)
        digits: Digits = []
        while value:
            value, digit = divmod(value, BASE)
            digits.append(digit)
        return cls._normalize(digits if digits else [0], sign)

    def to_int(self) -> int:
        """Возвращает значение как встроенный int (для тестов)."""
        value = 0
        for digit in reversed(self.digits):
            value = value * BASE + digit
        return -value if self.sign < 0 else value

    def __repr__(self) -> str:
        return f"BigInt({self.to_int()})"

    # --- реализуйте: разбор и печать --------------------------------------

    @classmethod
    def from_string(cls, value: str, base: int = 10) -> BigInt:
        """Разбирает строку в BigInt.

        Требования:
        - основания: 2, 8, 10, 16 (другие — ValueError);
        - строка может иметь ведущий ``+``/``-`` и пробелы по краям;
        - для 2/8/16 допускаются префиксы ``0b``/``0o``/``0x``;
        - ``_`` допустим только между цифрами;
        - недопустимая цифра/пустая строка — ValueError;
        - тип аргумента не str — TypeError.
        """
        raise NotImplementedError("реализуйте BigInt.from_string")

    def to_string(self, base: int = 10) -> str:
        """Строковое представление: без префиксов, с ведущим ``-``.

        Основания: 2, 8, 10, 16 (другие — ValueError).
        """
        raise NotImplementedError("реализуйте BigInt.to_string")


# --- реализуйте: арифметика и сравнение -----------------------------------


def neg(a: BigInt) -> BigInt:
    """-a"""
    raise NotImplementedError("реализуйте neg")


def add(a: BigInt, b: BigInt) -> BigInt:
    """a + b"""
    raise NotImplementedError("реализуйте add")


def sub(a: BigInt, b: BigInt) -> BigInt:
    """a - b"""
    raise NotImplementedError("реализуйте sub")


def mul(a: BigInt, b: BigInt) -> BigInt:
    """a * b"""
    raise NotImplementedError("реализуйте mul")


def compare(a: BigInt, b: BigInt) -> int:
    """-1, 0 или 1: a < b, a == b, a > b."""
    raise NotImplementedError("реализуйте compare")