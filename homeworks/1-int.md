## Теория

База:
- Как хранятся числа в памяти? http://www.5byte.ru/11/0008.php
- Как устроен `int` внутри? https://www.codementor.io/@arpitbhayani/python-caches-integers-16jih595jk
- Super long `int` in Python: https://www.youtube.com/watch?v=FNuwKuVF8Y0
- `int` interning (`x, y = 1, 1; id(x) == id(y) # True`): https://www.codesansar.com/python-programming/integer-interning.htm
- Immortal `int`s: https://peps.python.org/pep-0683/

Исходники:
- `int`: https://github.com/python/cpython/blob/main/Objects/longobject.c

Документация:
- `numbers.py`: https://docs.python.org/3/library/numbers.html
- Дополнительные методы на `int`: https://docs.python.org/3/library/stdtypes.html?highlight=str#additional-methods-on-integer-types

## Практика

Реализуй упрощённый аналог `PyLong` из CPython — **целое произвольной
точности (BigInt)**: своё сложение, вычитание, умножение и сравнение чисел
любой длины, в том числе не помещающихся в `sys.maxsize`.

- Задание и шаблон: `practice/bigint`
- Проверка: заготовленные тесты, `make test` (или `make docker-test`)

Уровни (по аналогии с лекцией):

- **Junior**: разбор строки и печать в десятичной системе.
- **Middle**: арифметика со знаком и сравнение; числа из сотен разрядов.
- **Senior**: основания `2/8/16`, префиксы `0b`/`0o`/`0x`, `_` между цифрами
  (как в литералах `0xa_0`, `1_60` из лекции); понимание, почему у
  `PyLong` основание системы счисления — степень двойки.

Бонус-идеи для своих проектов:
- реализовать то же самое, но на C (с `malloc`/`free` и битовым основанием);
- добавить `__add__`, `__sub__`, `__mul__`, `__lt__` и прочие dunder-методы,
  чтобы `BigInt` вёл себя как настоящий `int`;
- ускорить умножение алгоритмом Карацубы вместо школьного `O(n·m)`.
