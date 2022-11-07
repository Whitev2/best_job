import psycopg2
from psycopg2 import sql
from sqlalchemy.ext.declarative import declarative_base

from loader import all_data

BaseModel = declarative_base()


async def sql_delete(table_name, condition_dict):
    try:
        data = all_data()
        con = data.get_postgres()

        safe_query = sql.SQL("DELETE from {} WHERE {} = {};").format(sql.Identifier(table_name), sql.SQL(', ').join(
            map(sql.Identifier, condition_dict)), sql.SQL(", ").join(map(sql.Placeholder, condition_dict)))

        with con.cursor() as cur:
            cur.execute(safe_query, condition_dict)

        con.commit()
        con.close()
    except (psycopg2.Error, IndexError) as error:
        return False


async def sql_safe_select(column, table_name, condition_dict):
    try:
        data = all_data()
        con = data.get_postgres()
        ident_list = list()
        if isinstance(column, list):
            for i in column:
                ident_list.append(sql.Identifier(i))
        elif isinstance(column, str):
            ident_list.append(sql.Identifier(column))
        safe_query = sql.SQL("SELECT {col_names} from {} WHERE {} = {};").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier,
                                   condition_dict)),
            sql.SQL(", ").join(map(sql.Placeholder,
                                   condition_dict)),
            col_names=sql.SQL(',').join(ident_list)
        )
        with con.cursor() as cur:
            cur.execute(safe_query, condition_dict)
            data = cur.fetchall()
        con.commit()
        con.close()
        if isinstance(column, list):
            return data[0]
        else:
            return data[0][0]
    except IndexError as err:
        return False
    except (psycopg2.Error, IndexError) as error:
        return False


async def sql_safe_insert(table_name, values_dict: dict):
    try:
        data = all_data()
        con = data.get_postgres()
        safe_query = sql.SQL("INSERT INTO {} ({}) VALUES ({});").format(sql.Identifier(table_name),
                                                                        sql.SQL(', ').join(map(sql.Identifier,
                                                                                               values_dict)),
                                                                        sql.SQL(", ").join(map(sql.Placeholder,
                                                                                               values_dict)))
        with con.cursor() as cur:
            cur.execute(safe_query, values_dict)
        con.commit()
        con.close()
    except (psycopg2.Error, IndexError) as error:
        return False

async def sql_safe_update(table_name, data_dict, condition_dict):
    try:
        data = all_data()
        con = data.get_postgres()
        assert data_dict != {}, 'You have empty datadict in updater'
        assert data_dict != {}, 'You have empty conditiondict in updater'
        where = list(condition_dict.keys())[0]
        equals = condition_dict[where]
        safe_query = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {};").format(sql.Identifier(table_name),
                                                                            sql.SQL(', ').join(
                                                                                map(sql.Identifier, data_dict)),
                                                                            sql.SQL(", ").join(
                                                                                map(sql.Placeholder, data_dict)),
                                                                            sql.Identifier(where), sql.Literal(equals))

        with con.cursor() as cur:
            cur.execute(safe_query, data_dict)
        return "Complete"
    except AssertionError as error:
        print(error)
    except psycopg2.Error as error:
        print(error)


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

async def sql_count_rows():
    try:
        data = all_data()
        con = data.get_postgres()
        with con.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM orders")
            data = cur.fetchall()
        return data
    except psycopg2.Error as error:
        return error


async def sql_get_last_rows(user_id: str, limit: str = 1):
    try:
        data = all_data()
        con = data.get_postgres()
        query = 'SELECT * FROM orders WHERE "Executor_id" = %s ORDER BY id DESC LIMIT %s'
        record = (user_id, limit,)
        print(record)
        with con.cursor() as cur:
            cur.execute(query, record)
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

