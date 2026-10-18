"""Упрощённый `int` произвольной точности — домашка к лекции «1-int».

Публичный API:
- ``BigInt.from_int(value)`` / ``BigInt.from_string(value, base)``
- ``bi.to_int()`` / ``bi.to_string(base)``
- ``add(bi1, bi2)``, ``sub(bi1, bi2)``, ``mul(bi1, bi2)``
- ``neg(bi)``, ``compare(bi1, bi2)``
"""

from bigint.bigint import BigInt, add, compare, mul, neg, sub

__all__ = ["BigInt", "add", "compare", "mul", "neg", "sub"]