import os
import psycopg2
from aiogram import Bot
from redis import from_url


class all_data:
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.pg_db = os.getenv('POSTGRES_BASE')
        self.pg_user = os.getenv('POSTGRES_USER')
        self.pg_pswd = os.getenv('POSTGRES_PASSWORD')
        self.pg_host = os.getenv('POSTGRES_HOST')
        self.pg_port = os.getenv('POSTGRES_PORT')
        self.driver_group = "-1001695448061"
        self.info_channel = "-1001810427568"
        self.super_admins = (2036190335, 2133981686)

# функции для подключения к базам и токен
    def get_bot(self):
        return Bot(self.bot_token, parse_mode="HTML")

    def get_postgres(self):
        return psycopg2.connect(database=self.pg_db, user=self.pg_user, password=self.pg_pswd, host=self.pg_host, port=int(self.pg_port))

    def get_red(self):
        return from_url(self.redis_url, decode_responses=True)

    def get_data_red(self):
        return from_url(f'{self.redis_url}/1', decode_responses=True)

