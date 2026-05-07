import asyncpg
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI

import schemas
from log import get_logger

load_dotenv()

dsn = os.getenv('DATABASE_URL')
if not dsn:
    raise ValueError('Нет DATABASE_URL в файле .env')
admin_password = os.getenv('ADMIN_PASSWORD')
if not admin_password:
    raise ValueError('Нет ADMIN_PASSWORD в файле .env')
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=5,
        max_size=10,
    )
    logger.info('Пул соединений установлен')
    async with app.state.pool.acquire() as session:
        await session.execute('create table if not exists users (id serial primary key, name varchar(60), age integer, email varchar(45) unique, reg_time timestamp default now())')
        await session.execute('create index if not exists idx_regtime_desc on users(reg_time desc)')
    yield
    logger.info('Пул соединений разорван')
    await app.state.pool.close()

async def get_users_db(pool):
    async with pool.acquire() as session:
        data = await session.fetch('select * from users order by reg_time desc limit 50')
    if not data:
        return schemas.ReturnForm(success=False, message='База данных пуста', error_code='empty')
    return schemas.ReturnForm(success=True, message=f'Найдено {len(data)} пользователей.', data=[dict(row) for row in data])

async def add_user_db(pool, user_data: schemas.UserDataForm):
    async with pool.acquire() as session:
        logger.info('Попытка создать пользователя')
        try:
            user_id = await session.fetchval('insert into users (name, age, email) values ($1, $2, $3) returning id', user_data.name, user_data.age, user_data.email)
            logger.info(f'Пользователь {user_data.email} создан, id={user_id}')
            return schemas.ReturnForm(success=True, message=f'Успешно добавлен пользователь по айди {user_id}')
        except asyncpg.UniqueViolationError:
            logger.error('Пользователь с ввел существующий email')
            return schemas.ReturnForm(success=False, message=f'Пользователь с email \'{user_data.email}\' уже существует', error_code='conflict')
        except Exception as e:
            logger.error(f'Ошибка {e}')
            return schemas.ReturnForm(success=False, message='Ошибка на стороне сервера')
        
async def clear_all_db(pool, password: schemas.PasswordForm):
    logger.info('Попытка очистить базу данных')
    if password.password != admin_password:
        logger.error('Был введён неверный пароль')
        return schemas.ReturnForm(success=False, message='Неверный админ-пароль', error_code='unauthorized')
    async with pool.acquire() as session:
        deleted = await session.fetchval('select count(*) from users')
        await session.execute('truncate users restart identity')
    logger.info(f'База данных очищена, удалено {deleted} записей.')
    return schemas.ReturnForm(success=True, message=f'Удалено {deleted} записей.')

async def delete_user_db(pool, user_id: schemas.UserIdForm, password: schemas.PasswordForm):
    logger.info(f'Попытка удалить пользователя по айди {user_id.id}')
    if password.password != admin_password:
        logger.error('Был введен неверный пароль')
        return schemas.ReturnForm(success=False, message='Неверный админ-пароль', error_code='unauthorized')
    async with pool.acquire() as session:
        try:
            deleted_data = await session.fetch('delete from users where id=$1 returning *', user_id.id)
            if not deleted_data:
                logger.error(f'Пользователя по айди {user_id.id} не существует')
                return schemas.ReturnForm(success=False, message='Нет такого пользователя', error_code='unknown_user')
        except Exception as e:
            logger.error(f'Ошибка {e}')
            return schemas.ReturnForm(success=False, message='Ошибка внутри сервера', error_code='server_error')
    logger.info(f'Пользователь по айди {user_id.id} удален')
    return schemas.ReturnForm(success=True, message=f'Удален пользователь под айди {user_id.id}', data=[dict(row) for row in deleted_data])