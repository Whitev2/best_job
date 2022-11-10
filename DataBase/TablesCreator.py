import psycopg2

from loader import all_data

data = all_data()


def tables_god():
    try:
        con = data.get_postgres()
        cur = con.cursor()
        cur.execute("SELECT version();")
        record = cur.fetchone()
        print(f"You connect to - {record}, \n")


        cur.execute('''CREATE TABLE IF NOT EXISTS public.users(
                     "user_id" TEXT NOT NULL PRIMARY KEY,
                     "username" TEXT NOT NULL,
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
                     "DateTime_order" TEXT,
                     "order_time" TEXT,
                     "extradition" json,
                     "status" BOOL,
                     "Executor_id" TEXT,
                     "price" FLOAT,
                     FOREIGN KEY ("Executor_id")  REFERENCES users (user_id)
                     )''')
        con.commit()
        con.close()

    except psycopg2.Error as e:
        print(e)