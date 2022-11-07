import psycopg2

from loader import all_data

data = all_data()


def tables_god():
    try:
        con = data.get_postgres()
        # Курсор для выполнения операций с базой данных
        cur = con.cursor()

        # Выполнение SQL-запроса
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f"You connect to - {record}, \n")

        # Создание таблиц

        cur.execute('''CREATE TABLE IF NOT EXISTS public.users(
                     "user_id" TEXT NOT NULL,
                     "username" TEXT NOT NULL PRIMARY KEY,
                     "DateTime_come" TEXT,
                     "name" TEXT,
                     "car_number" TEXT,
                     "car_mass" TEXT)''')

        cur.execute('''CREATE TABLE IF NOT EXISTS public.texts(
                     "text" TEXT NOT NULL,
                     "tag" TEXT NOT NULL PRIMARY KEY
                     )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS public.orders(
                     "id" INTEGER NOT NULL PRIMARY KEY,
                     "Executor_id" TEXT,
                     "DateTime_order" TEXT,
                     "extradition" json
                     )''')
        con.commit()
        con.close()

    except psycopg2.Error as e:
        print(e)