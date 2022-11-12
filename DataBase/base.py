import psycopg2
from psycopg2 import sql
from sqlalchemy.ext.declarative import declarative_base

from loader import all_data

BaseModel = declarative_base()

data = all_data()
class User:

    def __init__(self):
        self.data = all_data()


    async def get_user_info(self, user_id, column):
        con = self.data.get_postgres()
        sql_query = "SELECT {} FROM users WHERE user_id = {}".format(column, f"'{user_id}'")
        with con.cursor() as cur:
            cur.execute(sql_query)
            data = cur.fetchall()
            return data


    async def sql_delete(self, table_name, condition_dict):
        try:
            con = self.data.get_postgres()
            safe_query = sql.SQL("DELETE from {} WHERE {} = {};").format(sql.Identifier(table_name), sql.SQL(', ').join(
                map(sql.Identifier, condition_dict)), sql.SQL(", ").join(map(sql.Placeholder, condition_dict)))

            with con.cursor() as cur:
                cur.execute(safe_query, condition_dict)

            con.commit()
        except (psycopg2.Error, IndexError) as error:
            return False

    async def sql_update(self, table, update_dict, condition_dict):
        try:
            con = self.data.get_postgres()
            set_poin = list(update_dict.keys())[0]
            equals = update_dict[set_poin]
            where = list(condition_dict.keys())[0]
            point = condition_dict[where]
            query = "UPDATE {} SET {} = {}  WHERE {} = {};".format(f'"{table}"', f'"{set_poin}"', f"'{equals}'",
                                                                   f'"{where}"', f"'{point}'")
            with con.cursor() as cur:
                cur.execute(query)
                con.commit()
        except psycopg2.Error as error:
            return error

    async def get_username(self, user_id):
        data = await self.get_user_info(user_id, 'username')
        return data[0][0]

    async def get_car_number(self, user_id):
        data = await self.get_user_info(user_id, 'car_number')
        return data[0][0]
    async def get_car_mass(self, user_id):
        data = await self.get_user_info(user_id, 'car_mass')
        return data[0][0]

    async def get_balance(self, user_id):
        data = await self.get_user_info(user_id, "balance")
        return data[0][0]



class Order():
    def __init__(self):
        self.data = all_data()

    async def get_last_order(self, user_id: str, limit: int = 1):
        try:
            con = self.data.get_postgres()
            query = 'SELECT * FROM orders WHERE "Executor_id" = %s ORDER BY id DESC LIMIT %s'
            record = (user_id, limit,)

            with con.cursor() as cur:
                cur.execute(query, record)
                data = cur.fetchall()
                print(data)
            return data
        except psycopg2.Error as error:
            return error

    async def sql_update_orders(self, column, user_id, condition_dict):
        try:
            con = self.data.get_postgres()
            where = list(condition_dict.keys())[0]
            equals = condition_dict[where]

            last_row = await self.get_last_order_id(user_id)
            id = last_row
            query = "UPDATE {} SET {} = {}  WHERE {} = {};".format(f'"{column}"', f'"{where}"',
                                                                   f"'{equals}'", f'"id"', id)
            with con.cursor() as cur:
                cur.execute(query)
                con.commit()
        except psycopg2.Error as error:
            return error

    async def get_last_order_id(self, user_id):
        data = await self.get_last_order(user_id)
        return data[0][0]

    async def get_last_order_time(self, user_id):
        data = await self.get_last_order(user_id)
        return data[0][2]
    async def get_last_order_addresses(self, user_id):
        data = await self.get_last_order(user_id)
        return data[0][2]
    async def get_last_order_price(self, user_id):
        data = await self.get_last_order(user_id)
        return data[0][-1]

    async def get_count_rows(self):
        try:
            con = self.data.get_postgres()
            with con.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM orders")
                data = cur.fetchall()
            return data
        except psycopg2.Error as error:
            return error


async def sql_safe_insert(table_name, values_dict: dict):
    try:
        con = data.get_postgres()
        safe_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(sql.Identifier(table_name),
                                                                        sql.SQL(', ').join(map(sql.Identifier,
                                                                                               values_dict)),
                                                                        sql.SQL(", ").join(map(sql.Placeholder,
                                                                                               values_dict)))
        with con.cursor() as cur:
            cur.execute(safe_query, values_dict)
            con.commit()
    except (psycopg2.Error, IndexError) as error:
        print(error)
        return False




async def data_getter(query, record=None):
    try:
        data = all_data()
        con = data.get_postgres()
        with con.cursor() as cur:
            cur.execute(query, (record,))
            data = cur.fetchall()
        return data
    except psycopg2.Error as error:
        return error






"""^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^DATA_REDIS^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"""


async def del_key(key):
    try:
        all_data().get_data_red().delete(key)
    except Exception as error:
        print(error)


async def list_write(key, value):
    try:
        all_data().get_data_red().rpush(key, value)
    except Exception as error:
        print(error)


async def list_read(key):
    try:
        return all_data().get_data_red().lrange(key, 0, -1)
    except Exception as error:
        print(error)


async def redis_just_one_write(key, value, ttl: int = None):
    try:
        all_data().get_data_red().set(key, value, ex=ttl)
    except Exception as error:
        print(error)


async def redis_just_one_read(key):
    try:
        return all_data().get_data_red().get(key)
    except Exception as error:
        print(error)


async def redis_check(key):
    try:
        return all_data().get_data_red().exists(key)
    except Exception as error:
        print(error)

