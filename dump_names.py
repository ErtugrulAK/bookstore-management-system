import psycopg2
import re
from pg_env import db_password

def normalize(text):
    if not text: return ""
    text = text.lower()
    tr_map = {
        'ı': 'i', 'İ': 'i', 'ş': 's', 'Ş': 's', 'ğ': 'g', 'Ğ': 'g',
        'ü': 'u', 'Ü': 'u', 'ö': 'o', 'Ö': 'o', 'ç': 'c', 'Ç': 'c'
    }
    for k, v in tr_map.items():
        text = text.replace(k, v)
    return re.sub(r'[^a-z0-9]', '', text)

conn = psycopg2.connect(f"host=localhost port=5432 dbname=kitapsatisdb user=postgres password={db_password()}")
cur = conn.cursor()
cur.execute('SELECT "Name" FROM "Books"')
books = cur.fetchall()
print([normalize(b[0]) for b in books])
