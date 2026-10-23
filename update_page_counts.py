import pandas as pd
import psycopg2
import json
import os
from pg_env import db_password

# 1. Read Excel
excel_path = 'Kitap Bilgileri.xlsx'
if not os.path.exists(excel_path):
    print(f"Error: {excel_path} not found.")
    exit(1)

df = pd.read_excel(excel_path)
# Clean column names
df.columns = [str(col).strip() for col in df.columns]

# Find relevant columns by keyword because of potential encoding issues
name_col = next((col for col in df.columns if 'Kitap' in col), None)
page_col = next((col for col in df.columns if 'Sayfa' in col), None)

if not name_col or not page_col:
    print(f"Error: Could not find Name or Page Count columns. Found: {df.columns.tolist()}")
    exit(1)

print(f"Matching using column: '{name_col}' and updating from: '{page_col}'")

# 2. Database Connection
db_config = {
    "host": "localhost",
    "database": "kitapsatisdb",
    "user": "postgres",
    "password": db_password(),
    "port": "5432"
}

try:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # Get all books from DB to match
    cur.execute('SELECT "Id", "Name" FROM "Books"')
    db_books = cur.fetchall()

    update_count = 0
    for db_id, db_name in db_books:
        # Find match in Excel
        # Use case-insensitive and stripped match
        match = df[df[name_col].str.strip().str.lower() == db_name.strip().lower()]
        
        if not match.empty:
            page_val = match.iloc[0][page_col]
            try:
                page_count = int(page_val)
                if page_count > 0:
                    cur.execute('UPDATE "Books" SET "PageCount" = %s WHERE "Id" = %s', (page_count, db_id))
                    update_count += 1
            except (ValueError, TypeError):
                continue

    conn.commit()
    print(f"Successfully updated {update_count} books in the database.")

    # 3. Update JSON file
    json_path = 'books_data_v2.json'
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            books_json = json.load(f)
        
        json_update_count = 0
        for book in books_json:
            match = df[df[name_col].str.strip().str.lower() == book['Name'].strip().lower()]
            if not match.empty:
                page_val = match.iloc[0][page_col]
                try:
                    book['PageCount'] = int(page_val)
                    json_update_count += 1
                except (ValueError, TypeError):
                    continue
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(books_json, f, ensure_ascii=False, indent=2)
        print(f"Successfully updated {json_update_count} books in {json_path}.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if 'conn' in locals():
        cur.close()
        conn.close()
