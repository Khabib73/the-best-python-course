"""Заготовленные тесты к домашке «1-int»: упрощённый аналог PyLong.

Запуск:  python3 -m pytest   (или  make test / make docker-test)
"""

import math
import random
import sys

import pytest

from bigint import BigInt, add, compare, mul, neg, sub

# --- конвертация в/из встроенного int ------------------------------------


@pytest.mark.parametrize(
    "value",
    [
        0,
        1,
        -1,
        2,
        -3,
        100,
        -100,
        42,
        -42,
        sys.maxsize,
        sys.maxsize + 1,
        -(sys.maxsize + 1),
        2**64,
        -2**64,
        2**100,
        10**30,
        -(10**30),
    ],
)
def test_from_to_int(value: int) -> None:
    assert BigInt.from_int(value).to_int() == value


# --- строковое представление ----------------------------------------------


@pytest.mark.parametrize(
    "value, string",
    [
        (0, "0"),
        (5, "5"),
        (-5, "-5"),
        (255, "255"),
        (10**20, "100000000000000000000"),
        (-(10**20), "-100000000000000000000"),
        (2**100, "1267650600228229401496703205376"),
    ],
)
def test_to_string_decimal(value: int, string: str) -> None:
    assert BigInt.from_int(value).to_string() == string


@pytest.mark.parametrize(
    "value, base, string",
    [
        (255, 16, "ff"),
        (-255, 16, "-ff"),
        (255, 8, "377"),
        (10, 8, "12"),
        (10, 2, "1010"),
        (2**100, 2, "1" + "0" * 100),
    ],
)
def test_to_string_other_bases(value: int, base: int, string: str) -> None:
    assert BigInt.from_int(value).to_string(base) == string


@pytest.mark.parametrize(
    "string, base, expected",
    [
        ("0", 10, 0),
        ("+42", 10, 42),
        ("-42", 10, -42),
        (" 123 ", 10, 123),
        ("1_000", 10, 1000),
        ("1_000_000", 10, 1000000),
        ("-1_0", 10, -10),
        ("ff", 16, 255),
        ("0xff", 16, 255),
        ("0XFF", 16, 255),
        ("0b1010", 2, 10),
        ("0o12", 8, 10),
        ("-0xff", 16, -255),
        ("010", 8, 8),
    ],
)
def test_from_string(string: str, base: int, expected: int) -> None:
    assert BigInt.from_string(string, base).to_int() == expected


# --- сложение и вычитание --------------------------------------------------


@pytest.mark.parametrize(
    "a, b",
    [
        (0, 0),
        (1, 2),
        (5, -5),
        (-5, 5),
        (-3, 7),
        (7, -3),
        (-7, 3),
        (2**60 - 1, 1),
        (2**60, 1),
        (10**20, -(10**19)),
        (-(10**20), 10**19),
        (sys.maxsize, sys.maxsize),
        (2**100, 2**100),
        (-(10**30), -(10**29)),
    ],
)
def test_add(a: int, b: int) -> None:
    assert add(BigInt.from_int(a), BigInt.from_int(b)).to_int() == a + b


@pytest.mark.parametrize(
    "a, b",
    [
        (0, 0),
        (5, 3),
        (3, 5),
        (5, 5),
        (0, 5),
        (5, 0),
        (2**60, 1),
        (1, 2**60),
        (10**30, 1),
        (-(10**30), 1),
        (-5, -3),
        (-3, -5),
    ],
)
def test_sub(a: int, b: int) -> None:
    assert sub(BigInt.from_int(a), BigInt.from_int(b)).to_int() == a - b


# --- умножение --------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b",
    [
        (0, 42),
        (42, 0),
        (6, 7),
        (-6, 7),
        (6, -7),
        (-6, -7),
        (2**30, 2**30),
        (2**30 - 1, 2**30 - 1),
        (2**60 - 1, 2**60 - 1),
        (123456, -789012),
        (10**50, 10**50),
        (123456789012345678901234567890, 987654321098765432109876543210),
    ],
)
def test_mul(a: int, b: int) -> None:
    assert mul(BigInt.from_int(a), BigInt.from_int(b)).to_int() == a * b


def test_factorial_100() -> None:
    result = BigInt.from_int(1)
    for i in range(2, 101):
        result = mul(result, BigInt.from_int(i))
    assert result.to_int() == math.factorial(100)


# --- сравнение --------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, 0),
        (1, 1, 0),
        (-5, -5, 0),
        (-5, 3, -1),
        (3, -5, 1),
        (1, 2, -1),
        (2, 1, 1),
        (10**30, 10**29, 1),
        (10**29, 10**30, -1),
        (-(10**30), -(10**29), -1),
        (-(10**29), -(10**30), 1),
    ],
)
def test_compare(a: int, b: int, expected: int) -> None:
    assert compare(BigInt.from_int(a), BigInt.from_int(b)) == expected


# --- знак -------------------------------------------------------------------


@pytest.mark.parametrize("value", [0, 1, -1, 12345, -(10**40)])
def test_neg(value: int) -> None:
    assert neg(BigInt.from_int(value)).to_int() == -value
    assert neg(neg(BigInt.from_int(value))).to_int() == value


# --- инварианты представления ----------------------------------------------


def test_normalized_digits() -> None:
    value = BigInt.from_int(0)
    assert value.sign == 0
    assert value.digits == [0]

    value = BigInt.from_int(2**61)
    assert value.sign == 1
    assert value.digits[-1] != 0
    assert all(0 <= digit < 2**30 for digit in value.digits)


# --- случайный стрес-тест ---------------------------------------------------


def test_random_round_trip() -> None:
    rnd = random.Random(42)
    for _ in range(200):
        value = rnd.getrandbits(rnd.randint(0, 512))
        if rnd.random() < 0.5:
            value = -value
        assert BigInt.from_int(value).to_int() == value


def test_random_arithmetic() -> None:
    rnd = random.Random(42)
    for _ in range(200):
        a = rnd.getrandbits(rnd.randint(0, 200))
        b = rnd.getrandbits(rnd.randint(0, 200))
        if rnd.random() < 0.5:
            a = -a
        if rnd.random() < 0.5:
            b = -b
        ba, bb = BigInt.from_int(a), BigInt.from_int(b)
        assert add(ba, bb).to_int() == a + b
        assert sub(ba, bb).to_int() == a - b
        assert mul(ba, bb).to_int() == a * b
        assert compare(ba, bb) == (a > b) - (a < b)


# --- ошибки -----------------------------------------------------------------


@pytest.mark.parametrize("string", ["", " ", "+", "-", "0x", "0xg", "12a", "12.5", "1_", "_1", "1__0", "0b2"])
def test_from_string_invalid(string: str) -> None:
    with pytest.raises(ValueError):
        BigInt.from_string(string)


@pytest.mark.parametrize("string, base", [("10", 0), ("10", 3), ("10", 36)])
def test_from_string_unsupported_base(string: str, base: int) -> None:
    with pytest.raises(ValueError):
        BigInt.from_string(string, base)


def test_from_string_digit_out_of_base() -> None:
    with pytest.raises(ValueError):
        BigInt.from_string("g", 16)
    with pytest.raises(ValueError):
        BigInt.from_string("2", 2)
    with pytest.raises(ValueError):
        BigInt.from_string("102", 2)


def test_type_errors() -> None:
    with pytest.raises(TypeError):
        BigInt.from_int("123")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        BigInt.from_string(123)  # type: ignore[arg-type]


def test_to_string_unsupported_base() -> None:
    with pytest.raises(ValueError):
        BigInt.from_int(42).to_string(3)