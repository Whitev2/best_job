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
