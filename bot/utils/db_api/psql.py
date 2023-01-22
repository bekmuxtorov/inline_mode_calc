from datetime import datetime
from pytz import timezone
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(
            self, command, *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}"
            for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    '''User queries'''

    async def user_exists(self, id: int):
        sql = "select lang from users_user where id = $1;"
        user_lang = await self.execute(sql, id, fetchval=True)
        if user_lang:
            return user_lang
        else:
            return False

    async def get_user(self, **kwargs):
        sql = """
        select id, lang, full_name, phone_number, region_id, who_is, workplace, created_at
        from users_user where
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        user = await self.execute(sql, *parameters, fetchrow=True)
        if user is not None:
            return {
                "id": user[0],
                "lang": user[1],
                "full_name": user[2],
                "phone_number": user[3],
                "region_id": user[4],
                "who_is": user[5],
                "workplace": user[6],
                "created_at": user[7]
            }
        return None

    async def get_users_by(self, **kwargs):
        sql = '''
            select id, phone_number, full_name
            from users_user where
        '''
        sql, parameters = self.format_args(sql, parameters=kwargs)
        users = await self.execute(sql, *parameters, fetch=True)
        return tuple(
            {
                "id": user[0],
                "phone_number": user[1],
                "full_name": user[2]
            }
            for user in users
        )

    async def create_request(self, user_info: dict):
        id = user_info["id"]
        full_name = user_info["first_name"]
        username = user_info["username"]
        created_at = datetime.now(tz=timezone("Asia/Tashkent"))
        if not all((id, full_name, username)):
            return False
        sql = '''
            insert into requests_request
            (id, full_name, username,created_at)
            values ($1, $2, $3, $4);
        '''
        try:
            await self.execute(
                sql, id, full_name, username, created_at, execute=True)
        except asyncpg.UniqueViolationError:
            return False
        return True

    '''Region queries'''

    async def get_regions(self, lang: str = "uz"):
        if lang not in ["uz", "ru", "en"]:
            lang = "uz"
        sql = f"select id, name_{lang} from users_region;"
        regions = await self.execute(sql, fetch=True)
        return {region[0]: region[1] for region in regions}
