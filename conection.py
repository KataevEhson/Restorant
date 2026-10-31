from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasw  = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="menu",
            password=pasw
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")
        
async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
        create table if not exists users(
            user_id serial primary key,
            full_name varchar(100),
            username varchar(100),
            telegram_id text,
            is_admin boolean default false,
            created_at timestamp default now(),
            is_active boolean default true
        );
        create table if not exists category(
            category_id serial primary key,
            category_name varchar(100),
            created_at timestamp default now(),
            is_active boolean default true
        );
        create table if not exists dishes(
            dish_id serial primary key,
            name varchar(100),
            caption text,
            file_id text,
            price int,
            category_id int references category(category_id),
            created_at timestamp default now(),
            is_active boolean default true
        );
        create table if not exists orders(
            order_id serial primary key,
            dish_id int references dishes(dish_id),
            telegram_id text,
            count int,
            created_at timestamp default now(),
            is_active boolean default true
        )

      """)
        print("Table created")
    except Exception as Error:
        print(f"Create Error: {Error}")
    finally:
        await conn.close()
        
        
        
        
    
        
        
        
async def send_photo(telegram_id, file_id, file_name):
    try:
        conn = await connection_db()
        await conn.execute("""
        INSERT INTO files(file_id, file_name, telegram_id) Values
        ($1, $2, $3)
                           """, file_id, file_name, str(telegram_id))
    except Exception as Error:
        print(f"Create photo error: {Error}")
    finally:
        await conn.close()
        
        
        
        
async def get_photo(telegram_id):
    try:
        conn = await connection_db()
        photos = await conn.fetch("""
        select * from files where telegram_id = $1
                           """,str(telegram_id))
        return photos
    except Exception as Error:
        print(f"get photo error: {Error}")
    finally:
        await conn.close()
        
        