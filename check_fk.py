import psycopg2
from pg_env import db_password
conn = psycopg2.connect(f"host=localhost port=5432 dbname=kitapsatisdb user=postgres password={db_password()}")
cur = conn.cursor()
cur.execute('SELECT conname, conrelid::regclass FROM pg_constraint WHERE confrelid = \'"Books"\'::regclass;')
print(cur.fetchall())
