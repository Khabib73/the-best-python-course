"""ЭТАЛОННОЕ РЕШЕНИЕ домашки «1-int» (для преподавателя/самопроверки).

Внимание, студентам: сначала попробуйте решить сами! :)

Полность работает с ``tests/test_bigint.py``:
    cp reference/bigint.py bigint/bigint.py && poetry run pytest

Упрощённый аналог `PyLong` из CPython: целое произвольной точности.
Число хранится в виде массива "цифр" (limbs) по основанию
``BASE = 2 ** SHIFT``, little-endian; знак — отдельно:

    value = sign * sum(digits[i] * BASE**i for i in range(len(digits)))
"""

from __future__ import annotations

SHIFT = 30          # PyLong_SHIFT в CPython
BASE = 1 << SHIFT   # 2 ** 30
MASK = BASE - 1     # PyLong_MASK

Digits = list[int]


def _digit_value(ch: str) -> int | None:
    """Числовое значение цифры 0-9, a-f или None."""
    if "0" <= ch <= "9":
        return ord(ch) - ord("0")
    lower = ch.lower()
    if "a" <= lower <= "f":
        return ord(lower) - ord("a") + 10
    return None


def _is_digit(ch: str, base: int) -> bool:
    value = _digit_value(ch)
    return value is not None and value < base


class BigInt:
    """Целое произвольной точности."""

    __slots__ = ("digits", "sign")

    def __init__(self, digits: Digits, sign: int) -> None:
        self.digits = digits
        self.sign = sign

    # --- каркас -----------------------------------------------------------

    @classmethod
    def _normalize(cls, digits: Digits, sign: int) -> BigInt:
        """Отбрасывает старшие нулевые разряды и обнуляет знак у нуля.

        ``sign == 0`` для ненулевого значения трактуется как «авто»:
        число положительное (так промежуточные результаты вроде
        ``_add_small``/``_mul_small`` не теряют знак).
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

    # --- разбор и печать --------------------------------------------------

    @classmethod
    def from_string(cls, value: str, base: int = 10) -> BigInt:
        """Разбирает строку в BigInt. Основания: 2, 8, 10, 16.

        Поддерживаются ведущий знак ``+``/``-``, префиксы ``0b``/``0o``/``0x``
        (если совпадают с основанием) и ``_`` между цифрами.
        """
        if not isinstance(value, str):
            raise TypeError(f"ожидалась строка, получено: {type(value).__name__}")
        if base not in (2, 8, 10, 16):
            raise ValueError(f"поддерживаются основания 2, 8, 10, 16; получено: {base}")

        text = value.strip()
        if not text:
            raise ValueError("пустая строка")

        sign = 1
        if text[0] in "+-":
            if text[0] == "-":
                sign = -1
            text = text[1:]
            if not text:
                raise ValueError("нет цифр после знака")

        prefix = {2: "0b", 8: "0o", 16: "0x"}.get(base)
        if prefix and len(text) >= 2 and text[:2].lower() == prefix:
            text = text[2:]
            if not text:
                raise ValueError(f"нет цифр после префикса {prefix!r}")

        cleaned: list[str] = []
        for i, ch in enumerate(text):
            if ch == "_":
                if i == 0 or i == len(text) - 1:
                    raise ValueError("символ '_' допустим только между цифрами")
                if not (_is_digit(text[i - 1], base) and _is_digit(text[i + 1], base)):
                    raise ValueError("символ '_' допустим только между цифрами")
            else:
                cleaned.append(ch)

        result = BigInt.from_int(0)
        for ch in cleaned:
            digit = _digit_value(ch)
            if digit is None or digit >= base:
                raise ValueError(f"цифра {ch!r} недопустима для основания {base}")
            result = _mul_small(result, base)
            result = _add_small(result, digit)

        if sign < 0:
            return neg(result)
        return result

    def to_string(self, base: int = 10) -> str:
        """Строковое представление: без префиксов, с ведущим ``-``."""
        if base not in (2, 8, 10, 16):
            raise ValueError(f"поддерживаются основания 2, 8, 10, 16; получено: {base}")
        if self.sign == 0:
            return "0"

        chars = "0123456789abcdef"
        result: list[str] = []
        value = BigInt(self.digits.copy(), 1)  # работаем с модулем числа
        while value.sign != 0:
            value, remainder = _divmod_small(value, base)
            result.append(chars[remainder])
        if self.sign < 0:
            result.append("-")
        return "".join(reversed(result))


# --- арифметика и сравнение -----------------------------------------------


def neg(a: BigInt) -> BigInt:
    """-a"""
    return BigInt(a.digits.copy(), -a.sign)


def add(a: BigInt, b: BigInt) -> BigInt:
    """a + b"""
    if a.sign == 0:
        return b
    if b.sign == 0:
        return a
    if a.sign == b.sign:
        return _add_abs(a, b, a.sign)
    order = _cmp_abs(a, b)
    if order == 0:
        return BigInt.from_int(0)
    if order > 0:
        return _sub_abs(a, b, a.sign)
    return _sub_abs(b, a, b.sign)


def sub(a: BigInt, b: BigInt) -> BigInt:
    """a - b"""
    return add(a, neg(b))


def mul(a: BigInt, b: BigInt) -> BigInt:
    """a * b — школьный алгоритм, O(n*m), как умножение в PyLong."""
    if a.sign == 0 or b.sign == 0:
        return BigInt.from_int(0)
    result: Digits = [0] * (len(a.digits) + len(b.digits))
    for i, da in enumerate(a.digits):
        carry = 0
        for j, db in enumerate(b.digits):
            total = result[i + j] + da * db + carry
            result[i + j] = total & MASK
            carry = total >> SHIFT
        result[i + len(b.digits)] = carry
    return BigInt._normalize(result, a.sign * b.sign)


def compare(a: BigInt, b: BigInt) -> int:
    """-1, 0 или 1: a < b, a == b, a > b."""
    if a.sign != b.sign:
        return 1 if a.sign > b.sign else -1
    if a.sign == 0:
        return 0
    order = _cmp_abs(a, b)
    if order == 0:
        return 0
    return order if a.sign > 0 else -order


# --- внутренние помощники (по модулю числа) -------------------------------


def _add_abs(a: BigInt, b: BigInt, sign: int) -> BigInt:
    size = max(len(a.digits), len(b.digits))
    result: Digits = [0] * size
    carry = 0
    for i in range(size):
        da = a.digits[i] if i < len(a.digits) else 0
        db = b.digits[i] if i < len(b.digits) else 0
        total = da + db + carry
        result[i] = total & MASK
        carry = total >> SHIFT
    if carry:
        result.append(carry)
    return BigInt._normalize(result, sign)


def _sub_abs(a: BigInt, b: BigInt, sign: int) -> BigInt:
    """Вычитает по модулю; требует |a| >= |b|."""
    result: Digits = []
    borrow = 0
    for i in range(len(a.digits)):
        da = a.digits[i]
        db = b.digits[i] if i < len(b.digits) else 0
        diff = da - db - borrow
        if diff < 0:
            diff += BASE
            borrow = 1
        else:
            borrow = 0
        result.append(diff)
    return BigInt._normalize(result, sign)


def _cmp_abs(a: BigInt, b: BigInt) -> int:
    if len(a.digits) != len(b.digits):
        return 1 if len(a.digits) > len(b.digits) else -1
    for i in range(len(a.digits) - 1, -1, -1):
        if a.digits[i] != b.digits[i]:
            return 1 if a.digits[i] > b.digits[i] else -1
    return 0


def _mul_small(a: BigInt, multiplier: int) -> BigInt:
    """a * multiplier, где multiplier — небольшое число (основание)."""
    carry = 0
    result: Digits = [0] * len(a.digits)
    for i, digit in enumerate(a.digits):
        total = digit * multiplier + carry
        result[i] = total & MASK
        carry = total >> SHIFT
    if carry:
        result.append(carry)
    return BigInt._normalize(result, a.sign)


def _add_small(a: BigInt, addend: int) -> BigInt:
    """a + addend, где addend — небольшое число (одна цифра)."""
    result: Digits = []
    carry = addend
    for digit in a.digits:
        total = digit + carry
        result.append(total & MASK)
        carry = total >> SHIFT
    while carry:
        result.append(carry & MASK)
        carry >>= SHIFT
    return BigInt._normalize(result, a.sign)


def _divmod_small(a: BigInt, divisor: int) -> tuple[BigInt, int]:
    """a // divisor и a % divisor, где divisor — небольшое положительное число."""
    if divisor <= 0:
        raise ValueError("делитель должен быть положительным")
    quotient: Digits = [0] * len(a.digits)
    remainder = 0
    for i in range(len(a.digits) - 1, -1, -1):
        current = (remainder << SHIFT) + a.digits[i]
        quotient[i] = current // divisor
        remainder = current % divisor
    return BigInt._normalize(quotient, a.sign), remainder