from fastapi import FastAPI, HTTPException
from models import Payment
from typing import List
from uuid import UUID, uuid4
import time, asyncio, mysql.connector, json

api = FastAPI()

def get_database_connection():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        user="freedb_khisrav",
        password="ASg?U3!&$x3hVjR",
        database="freedb_khisrav_api_db"
    )

async def database_query(query: str, values=None):
    connection = get_database_connection()
    cursor = connection.cursor()

    cursor.execute(query, values)
    if values:
        connection.commit()
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return result

async def payment_process(payment: Payment):
    service = await database_query("SELECT * FROM `services` WHERE `id` = %s", (payment.service_id,))
    wallet = await database_query("SELECT * FROM `wallets` WHERE `id` = %s", (payment.wallet_id,))

    if not service:
        status = "service not found"
    elif not wallet:
        status = "wallet not found"
    elif wallet[0][1] < payment.amount:
        status = "insufficient funds"
    else:
        status = "success"
        payment.amount = service[0][3]

        update_service_query = "UPDATE `services` SET `earnings` = `earnings` + %s WHERE `id` = %s"
        update_wallet_query = "UPDATE `wallets` SET `balance` = `balance` - %s WHERE `id` = %s"
        update_values = (payment.amount, payment.service_id)
        
        await database_query(update_service_query, update_values)
        await database_query(update_wallet_query, update_values)

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
    await database_query(sql_query, sql_values)

@api.post('/payment/')
async def create_payment(payment: Payment):
    payment.time = time.time()
    payment.uuid = uuid4()
    asyncio.create_task(payment_process(payment))
    return {
        "payment_uuid": payment.uuid,
        "message": "Payment is being processed"
    }

@api.get('/payment/{payment_uuid}')
async def check_payment(payment_uuid: str):
    payment = await database_query("SELECT * FROM `payments` WHERE `uuid` = '" + payment_uuid + "'")
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    payment_dict = {
        "id": payment[0][0],
        "uuid": payment[0][1],
        "amount": payment[0][2],
        "currency": payment[0][3],
        "time": payment[0][4],
        "wallet_id": payment[0][5],
        "service_id": payment[0][6],
        "status": payment[0][7]
    }
    return payment_dict
