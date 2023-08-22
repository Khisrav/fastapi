# fastapi
Простой тестовый код выполняющий следующие задачи:
1. Добавление нового платежа
2. Проверка статуса платежа
3. Снятие средств с баланса пользователей для оплаты услуги


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
mysql-connector-python
```
Также запустите скрипт ```setup.py```. Он отвечает за установку базы данных (файл ```mysql.sql```)

## Запуск
Команда для запуска REST API
```bash
uvicorn main:api
```

## Запросы
### Добавление нового платежа
```POST /payment/``` 
Пример входных параметров:
```JSON
{
  "wallet_id": 1,
  "service_id": 2
}
```
Пример ответа:
```JSON
{
  "payment_uuid": "7fcf5621-9803-4225-b113-e2421438f29a",
  "message": "Payment is being processed"
}
```
### Проверка статуса платежа
```GET /payment/{payment_uuid}```

Пример запроса: ```/payment/e4fd74f9-a8c1-4602-b28a-22855d8f6e20```

Пример ответа: 
```JSON
{
  "id": 10,
  "uuid": "e4fd74f9-a8c1-4602-b28a-22855d8f6e20",
  "amount": 99,
  "currency": "TJS",
  "time": 1692675455,
  "wallet_id": 1,
  "service_id": 1,
  "status": "insufficient funds"
}
```
