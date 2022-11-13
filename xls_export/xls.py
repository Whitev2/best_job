import xlsxwriter

from DataBase.base import data_getter


async def export_to_xls():
    workbook = xlsxwriter.Workbook('xls_export/orders.xlsx')
    orders_xls = workbook.add_worksheet('orders')
    users_xls = workbook.add_worksheet('users')
    users = await data_getter('SELECT * FROM users')
    orders = await data_getter('SELECT * FROM orders')

    users_xls.write('A1', 'Telegram_ID')
    users_xls.write('B1', 'Имя')
    users_xls.write('C1', 'Номер автомобиля')
    users_xls.write('D1', 'Вместимость автомобиля')
    users_xls.write('E1', 'Баланс')

    orders_xls.write('A1', 'ID')
    orders_xls.write('B1', 'Дата')
    orders_xls.write('C1', 'Время выполнения')
    orders_xls.write('D1', 'Исполнитель')
    orders_xls.write('E1', 'Стоимость')
    orders_xls.write('F1', 'Адреса')
    try:
        count = 2
        for user in users:
            users_xls.write(f'A{count}', user[0])
            users_xls.write(f'B{count}', user[1])
            users_xls.write(f'C{count}', user[3])
            users_xls.write(f'D{count}', user[5])
            users_xls.write(f'E{count}', user[4])
            count += 1
        count = 2
        #str(*order[3]).replace('//', ',')
        for order in orders:
            orders_xls.write(f'A{count}', order[0])
            orders_xls.write(f'B{count}', order[1])
            orders_xls.write(f'C{count}', order[2])
            orders_xls.write(f'D{count}', order[5])
            orders_xls.write(f'E{count}', order[6])
            orders_xls.write(f'F{count}', str(order[3]).replace('//', ','))
            count += 1
        workbook.close()
        return True
    except Exception as e:
        print(e)
