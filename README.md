# fastapi
Простой тестовый код выполняющий следующие задачи:
1. Добавление нового платежа
2. Проверка статуса платежа
3. Снятие средств с баланса пользователей
4. Пополнение средств баланса пользователей


## Установка
Для работы кода требуется Python 3.x и следующие библиотеки (некоторые из них возможно уже встроены в Python):
```bash
fastapi
uvicorn
uuid
models
typing
pydantic
enum
```

## Запуск
Команда для запуска REST API
```bash
uvicorn main:api
```

## Запросы
```GET``` Получает список существующих пользователей.
```
/users/
```
Пример ответа:
```JSON
[
  {
    "id": "cd0bdffa-9ee1-49a4-93bb-e93fb2e4d085",
    "fullname": "John Johnson",
    "wallet": 876.9,
    "currency": "TJS"
  },
  {
    "id": "13bdecd0-1a4b-43c1-bc60-87a5e4972df5",
    "fullname": "Don Carleon",
    "wallet": 246.2,
    "currency": "TJS"
  }
]
```
```POST``` Добавление нового платежа в базу
```
/payment/
```
Пример входных параметров:
```JSON
{
  "id": "13bdecd0-9ee1-49a4-93bb-87a5e4972df5",
  "amount": 123.1,
  "currency": "TJS",
  "time": 1691554986653,
  "sender": "cd0bdffa-9ee1-49a4-93bb-e93fb2e4d085",
  "receiver": "13bdecd0-1a4b-43c1-bc60-87a5e4972df5"
}
```
Пример ответа:
```JSON
{
  "status": "success"
}
```

```GET``` Проверяет статус платежа
```
/payment/{payment_id}
```
В качестве входного параметра принимается только ```ID``` платежа. Пример:
```
/payment/cd0bdffa-9ee1-49a4-93bb-87a5e4972df5
```
Пример ответа:
```
{
  "status": "found"
}
```
