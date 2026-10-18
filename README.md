# The Best Python Course

Бесплатный видеокурс, который разбирает Python «изнутри»: каждая тема
рассматривается со всех сторон и на трёх уровнях сложности —
**Junior**, **Middle**, **Senior**.

- Автор курса: [Nikita Sobolev](https://github.com/sobolevn) —
  [оригинальный репозиторий](https://github.com/sobolevn/the-best-python-course)
- Домашки и доработки: [Khabib Shakhbanov](https://github.com/khabib73)
- Лицензия: [CC BY-NC-SA 4.0](LICENSE)

Это производный репозиторий от
[`sobolevn/the-best-python-course`](https://github.com/sobolevn/the-best-python-course).

## Как устроен курс

| Папка | Что внутри |
|-------|------------|
| [`lectures/`](lectures/README.md) | Слайды лекций (Keynote `.key`) |
| [`homeworks/`](homeworks/1-int.md) | Домашки: теория и практические задания |
| [`practice/`](practice/asm-builtins/README.md) | Проекты для практики (шаблон + заготовленные тесты) |
| [`pdf/`](pdf/README.md) | PDF-версии лекций (сгенерированы из `.key`) |
| [`editing/`](editing/README.md) | Инструменты для работы с субтитрами |
| [`minimal_vscode/`](minimal_vscode/README.md) | Минимальный плагин VSCode для демонстраций |

## Домашки

| Лекция | Слайды | Теория | Практика |
|--------|--------|--------|----------|
| 0. Интро: устройство курса | [`0-intro.key`](lectures/0-intro.key) | — | — |
| 1. `int` | [`1-int.key`](lectures/1-int.key) | [`1-int.md`](homeworks/1-int.md) | [`practice/bigint`](practice/bigint/README.md) |

Как решать домашку:

1. Прочитай задание в соответствующей папке [`practice/`](practice/).
2. Реализуй недостающий код в шаблоне.
3. Проверь себя тестами:

```bash
cd practice/bigint
make install     # poetry install
make test        # poetry run pytest
```

Тесты можно запустить и в Docker, ничего не устанавливая на машину:

```bash
make docker-test
```

## Сообщество

- Discord: <https://discord.python.ru>
- Boosty (поддержка автора): <https://boosty.to/sobolevn>

## Лицензия

Материалы курса распространяются по лицензии
[Attribution-NonCommercial-ShareAlike 4.0 International](LICENSE)
(CC BY-NC-SA 4.0): можно делиться и перерабатывать с указанием авторства,
но только в некоммерческих целях и на тех же условиях.