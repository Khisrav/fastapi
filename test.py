import mysql.connector
def database_query(query: str):
    dataBase1 = mysql.connector.connect(
        host     = 'localhost',
        user     = 'root',
        password = '',
        database = 'fastapi'
    )

    cursorObject = dataBase1.cursor()

    # sql_query  = "INSERT INTO `payments` (`uuid`, `amount`, `currency`, `time`, `wallet_id`, `service_id`) VALUES (%s, %s, %s, %s, %s, %s)"
    # sql_values = (
    #     str(payment.uuid),
    #     payment.amount,
    #     payment.currency,
    #     payment.time,
    #     payment.wallet_id,
    #     payment.service_id
    # )

    # cursorObject.execute(sql_query, sql_values)
    cursorObject.execute(query)
    # dataBase1.commit()
    result = cursorObject.fetchall()
    dataBase1.close()
    return result

service = database_query("SELECT * FROM `services` WHERE `id` = " + str(1))
print(service)
if (len(service) != 0):
    # service exists
    pass