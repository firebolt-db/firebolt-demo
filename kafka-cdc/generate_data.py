from datetime import datetime
import psycopg2
from psycopg2 import sql
from faker import Faker
import random
import time
import argparse
import numpy as np

def create_tables(cursor):
    scores_table_sql = sql.SQL("""
        CREATE TABLE IF NOT EXISTS scores (
            user_id    INTEGER NOT NULL,
            level_id   INTEGER NOT NULL,
            created_at TIMESTAMP NOT NULL,
            score      INTEGER NOT NULL,
            PRIMARY KEY (user_id, level_id, created_at)
        );
    """)
    users_table_sql = sql.SQL("""
        CREATE TABLE IF NOT EXISTS users (
            id         SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name  VARCHAR(255) NOT NULL,
            gender     VARCHAR(50),
            address    TEXT
        );
    """)
    cursor.execute(scores_table_sql)
    cursor.execute(users_table_sql)


def insert_random_data(values_per_batch):
    # Database connection parameters
    db_config = {
        'dbname': 'postgres',
        'user': 'demouser',
        'password': 'localdemopassword',
        'host': 'localhost',
        'port': '5432',
    }
    
    # Establish connection
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        create_tables(cursor)
        fake = Faker()

        fetch_largest_id_sql = sql.SQL("""
            SELECT COUNT(id) FROM USERS;
        """)
        cursor.execute(fetch_largest_id_sql)
        start_index = cursor.fetchone()[0] + 1 or 1
        batch_start = start_index
        
        # Generate random user data
        for i in range(start_index, start_index + 100000):
            if random.randint(0, 1) == 0:
                first_name = fake.first_name_female()
                gender = 'female'
            else:
                first_name = fake.first_name_male()
                gender = 'male'
            
            if random.randint(0, 100) == 100:
                gender = 'other'
            
            last_name = fake.last_name()
            address = fake.address()
        
            # Insert data to both tables
            user_insert_query = sql.SQL("""
                INSERT INTO users (id, first_name, last_name, gender, address)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """)
            cursor.execute(user_insert_query, (i, first_name, last_name, gender, address))

            for n in range(1, 9):
                score = int(np.random.lognormal(mean=np.log(1_000_000), sigma=1.0))
                score_insert_query = sql.SQL("""
                    INSERT INTO scores (user_id, level_id, created_at, score)
                    VALUES (%s, %s,%s, %s);
                """)
                cursor.execute(score_insert_query, (i, n, datetime.now(), score))
        
            conn.commit()

            if i % values_per_batch == 0:
                print('Added records for IDs %d - %d' % (batch_start, i))
                batch_start = i+1
                time.sleep(5)
        
        
        # Close connection
        cursor.close()
        conn.close()

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insert sequential data into PostgreSQL")
    parser.add_argument("values_per_batch", type=int, help="Number of values to write to Postgres every 5 seconds")
    args = parser.parse_args()
    insert_random_data(args.values_per_batch)