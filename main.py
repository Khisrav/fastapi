from fastapi import FastAPI, HTTPException
from models import Payment
from typing import List
from uuid import UUID, uuid4
import time, asyncio, mysql.connector, json

api = FastAPI()

async def database_query(query: str, values = None):
    dataBase1 = mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = '',
        database = 'fastapi'
    )

    cursorObject = dataBase1.cursor()

    cursorObject.execute(query, values)
    if values:dataBase1.commit()
    result = cursorObject.fetchall()
    dataBase1.close()
    return result

async def payment_process(payment: Payment):
    # Check if service_id and wallet_id exists
    service = await database_query("SELECT * FROM `services` WHERE `id` = " + str(payment.service_id))
    wallet = await database_query("SELECT * FROM `wallets` WHERE `id` = " + str(payment.wallet_id))
    
    status = "success"
    if len(service) == 0:status = "service not found"
    if len(wallet) == 0:status = "wallet not found"
    
    # Update service earnings and wallet balance
    if (len(service) != 0 and len(wallet) != 0):
        payment.amount = service[0][3]    
        if len(wallet) != 0 and wallet[0][1] >= payment.amount:
            update_query = "UPDATE `services` SET `earnings` = `earnings` + %s WHERE `id` = %s"
            values = (payment.amount, payment.service_id)

            update_service = await database_query(update_query, values)
            ##############
            update_query = "UPDATE `wallets` SET `balance` = `balance` - %s WHERE `id` = %s"
            values = (payment.amount, payment.wallet_id)

            update_wallet = await database_query(update_query, values)
        elif len(wallet) != 0 and wallet[0][1] < payment.amount:status = "insufficient funds"

    # Add payment to DB with matching status
    sql_query = "INSERT INTO `payments` (`uuid`, `amount`, `currency`, `time`, `wallet_id`, `service_id`, `status`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sql_values = (
        str(payment.uuid),
        payment.amount,
        payment.currency,
        payment.time,
        payment.wallet_id,
        payment.service_id,
        status
    )
    transaction = await database_query(sql_query, sql_values)

@api.post('/payment/')
async def create_payment(payment: Payment):
    payment.time = time.time()
    payment.uuid = uuid4()
    asyncio.create_task(payment_process(payment))
    return {
        "payment_uuid": payment.uuid,
        "message": "Платеж обрабатывается"
    }

@api.get('/payment/{payment_uuid}')
async def check_payment(payment_uuid: str):
    payment = await database_query("SELECT * FROM `payments` WHERE `uuid` = '"+payment_uuid+"'")
    payment_dict = {
        "id": payment[0][0],
        "uuid": payment[0][1],
        "amount": payment[0][2],
        "currency": payment[0][3],
        "time": payment[0][4],
        "wallet_id": payment[0][5],
        "service_id": payment[0][6],
        "status": payment[0][7],
    }
    return json.loads(json.dumps(payment_dict, indent=4))
