from fastapi import FastAPI, HTTPException
from typing import Optional
import time
import logging
from uuid import UUID, uuid4
import asyncio
import aiomysql
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api = FastAPI()

class Payment(BaseModel):
    uuid: Optional[UUID] = uuid4()
    amount: Optional[float] = 0
    currency: Optional[str] = "TJS"
    time: Optional[int] = None
    wallet_id: int
    service_id: int

async def get_database_pool():
    logger.warning('$ Connecting to database')
    return await aiomysql.create_pool(
        host="sql.freedb.tech",
        user="freedb_khisrav",
        password="ASg?U3!&$x3hVjR",
        db="freedb_khisrav_api_db",
        autocommit=True
    )

async def database_query(pool, query, values=None):
    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:
            await cursor.execute(query, values)
            if values:
                await connection.commit()
            result = await cursor.fetchall()
    logger.warning('$ MySQL query result - ' + str(result))
    return result

async def payment_process(pool, payment: Payment):
    async with pool.acquire() as connection:
        service = await database_query(pool, "SELECT * FROM `services` WHERE `id` = %s", (payment.service_id,))
        wallet = await database_query(pool, "SELECT * FROM `wallets` WHERE `id` = %s", (payment.wallet_id,))

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
            
            logger.warning('$ Updating balances')
            
            await database_query(pool, update_service_query, update_values)
            await database_query(pool, update_wallet_query, update_values)

        logger.warning('$ Inserting to database')
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
        main_query_result = await database_query(pool, sql_query, sql_values)
        logger.warning(main_query_result)

# Create payment endpoint
@api.post('/payment/')
async def create_payment(payment: Payment):
    payment.time = time.time()
    payment.uuid = uuid4()
    
    pool = await get_database_pool()
    asyncio.create_task(payment_process(pool, payment))
    
    return {
        "payment_uuid": payment.uuid,
        "message": "Payment is being processed"
    }

# Check payment endpoint
@api.get('/payment/{payment_uuid}')
async def check_payment(payment_uuid: str):
    pool = await get_database_pool()
    
    payment = await database_query(pool, "SELECT * FROM `payments` WHERE `uuid` = %s", (payment_uuid,))
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
