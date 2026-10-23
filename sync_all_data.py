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

# Use indices to avoid encoding/naming issues
# 0: Kitap Adı, 1: Fiyat, 2: Sayfa Sayısı, 3: Yayınevi, 4: Bölüm, 5: Dil, 
# 6: Yazar(lar), 7: Yıl, 8: Baskı Sayısı, 9: ISBN No, 10: Stok, 11: Açıklama
cols = df.columns.tolist()

def get_val(row, idx):
    if idx < len(row):
        val = row[idx]
        return val if not pd.isna(val) else None
    return None

# Database config
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

    cur.execute('SELECT "Id", "Name" FROM "Books"')
    db_books = cur.fetchall()

    updated_count = 0
    for db_id, db_name in db_books:
        # Match by name
        match = df[df.iloc[:, 0].str.strip().str.lower() == db_name.strip().lower()]
        
        if not match.empty:
            row = match.iloc[0]
            
            try:
                price = float(row[1]) if get_val(row, 1) is not None else 0.0
                page_count = int(row[2]) if get_val(row, 2) is not None else 0
                publisher = str(row[3]).strip() if get_val(row, 3) else None
                category = str(row[4]).strip() if get_val(row, 4) else None
                language = str(row[5]).strip() if get_val(row, 5) else 'Türkçe'
                author = str(row[6]).strip() if get_val(row, 6) else None
                
                year_val = get_val(row, 7)
                publication_year = int(year_val) if year_val is not None else None
                
                edition = str(row[8]).strip() if get_val(row, 8) else None
                isbn = str(row[9]).strip() if get_val(row, 9) else None
                stock = int(row[10]) if get_val(row, 10) is not None else 0
                description = str(row[11]).strip() if get_val(row, 11) else None

                cur.execute('''
                    UPDATE "Books" SET 
                        "Price" = %s,
                        "PageCount" = %s,
                        "StockQuantity" = %s,
                        "PublicationYear" = %s,
                        "Publisher" = %s,
                        "Category" = %s,
                        "Language" = %s,
                        "Author" = %s,
                        "Edition" = %s,
                        "ISBN" = %s,
                        "Description" = %s,
                        "IsActive" = %s
                    WHERE "Id" = %s
                ''', (
                    price, page_count, stock, publication_year, publisher, category, language, 
                    author, edition, isbn, description, (stock > 0), db_id
                ))
                updated_count += 1
            except Exception as e:
                print(f"Error updating '{db_name}': {e}")

    conn.commit()
    print(f"Database sync complete. Updated {updated_count} records.")

    # Update JSON file
    json_path = 'books_data_v2.json'
    if os.path.exists(json_path):
        updated_json = []
        for index, row in df.iterrows():
            try:
                name = str(row[0]).strip()
                if not name or pd.isna(row[0]): continue
                
                stock = int(row[10]) if get_val(row, 10) is not None else 0
                
                book = {
                    "Name": name,
                    "Price": float(row[1]) if get_val(row, 1) is not None else 0.0,
                    "PageCount": int(row[2]) if get_val(row, 2) is not None else 0,
                    "Publisher": str(row[3]).strip() if get_val(row, 3) else None,
                    "Category": str(row[4]).strip() if get_val(row, 4) else None,
                    "Language": str(row[5]).strip() if get_val(row, 5) else 'Türkçe',
                    "Author": str(row[6]).strip() if get_val(row, 6) else None,
                    "PublicationYear": int(row[7]) if get_val(row, 7) is not None else None,
                    "Edition": str(row[8]).strip() if get_val(row, 8) else None,
                    "ISBN": str(row[9]).strip() if get_val(row, 9) else None,
                    "StockQuantity": stock,
                    "Description": str(row[11]).strip() if get_val(row, 11) else None,
                    "IsActive": stock > 0,
                    "IsFeatured": False,
                    "MinStockLevel": 25
                }
                updated_json.append(book)
            except:
                continue
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(updated_json, f, ensure_ascii=False, indent=2)
        print(f"JSON file sync complete. {len(updated_json)} books processed.")

except Exception as e:
    print(f"Critical error: {e}")
finally:
    if 'conn' in locals():
        cur.close()
        conn.close()
