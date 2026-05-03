# F-Bank Testing

[![CI](https://github.com/timdobrynchenko/f-bank-testing/actions/workflows/ci.yml/badge.svg)](https://github.com/timdobrynchenko/f-bank-testing/actions/workflows/ci.yml)

Итоговое задание по курсу тестирования. Ручное и автоматизированное тестирование банковского сервиса для переводов F-Bank: поиск дефектов, оформление документации, Selenium-автотесты, GitHub Actions CI.

> **О статусе сборки**: красная сборка — это **ожидаемое и требуемое** поведение. Тесты на найденные дефекты намеренно падают по условию задания.

## Документация

- [Чек-лист ручного тестирования](docs/checklist.md) — 20 пунктов
- [Тестовые сценарии](docs/test-scenarios.md) — 5 сценариев
- Баг-репорты:
  - [Bug #1 — Некорректное округление комиссии](docs/bug-reports/bug-01-commission-rounding.md)
  - [Bug #2 — Принимается отрицательная сумма перевода](docs/bug-reports/bug-02-negative-amount.md)
  - [Bug #3 — Поле номера карты принимает 17 цифр](docs/bug-reports/bug-03-card-length.md)

## Найденные дефекты

| ID | Severity | Описание |
|---|---|---|
| Bug #1 | 🟡 Major | Комиссия рассчитывается с округлением до десятков рублей вместо единиц: при сумме 91 руб. комиссия = 0 вместо 9. |
| Bug #2 | 🔴 Critical | Поле суммы перевода принимает отрицательные значения, перевод с отрицательной суммой подтверждается банком. |
| Bug #3 | 🟡 Major | Поле номера карты принимает 17 цифр вместо ровно 16, как требует спецификация. |

## Локальный запуск

### 1. Запуск сервиса F-Bank

```bash
python3 -m http.server 8000 --directory dist
```

Открыть в браузере: `http://localhost:8000/?balance=30000&reserved=20001`

### 2. Запуск автотестов

Создание окружения и установка зависимостей:

```bash
python3 -m venv .venv
source .venv/bin/activate         # Linux / macOS
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
```

Запуск тестов:

```bash
# Все тесты с HTML-отчетом
pytest --html=report.html --self-contained-html

# Только тесты на баги (упадут)
pytest tests/test_bugs.py -v

# Только проходящие сценарии
pytest tests/test_happy_paths.py -v
```

**Ожидаемый результат**: `3 failed, 2 passed`. Три теста на дефекты падают — это требование задания. Два happy/sad path теста проходят и подтверждают, что инфраструктура работает корректно.

## Структура проекта

```
fbank-testing/
├── .github/workflows/ci.yml         # GitHub Actions
├── dist/                            # сервис F-Bank (статика)
├── docs/                            # тестовая документация
│   ├── checklist.md
│   ├── test-scenarios.md
│   └── bug-reports/
│       ├── bug-01-commission-rounding.md
│       ├── bug-02-negative-amount.md
│       ├── bug-03-card-length.md
│       └── screenshots/
├── tests/                           # Selenium-автотесты
│   ├── conftest.py
│   ├── pages/                       # Page Object
│   ├── test_bugs.py
│   └── test_happy_paths.py
├── requirements.txt
└── pytest.ini
```

## Стек

- Python 3.11
- Selenium 4 (headless Chrome)
- pytest + pytest-html
- GitHub Actions (Ubuntu runner)
