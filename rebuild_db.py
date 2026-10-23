import pandas as pd
import psycopg2
import math
import json
import os
from pg_env import db_password

def clean_value(val):
    if pd.isna(val) or val is None:
        return None
    if isinstance(val, float) and math.isnan(val):
        return None
    return str(val).strip()

def to_float(v):
    try:
        if pd.isna(v): return 0.0
        val = float(v)
        if math.isnan(val): return 0.0
        return val
    except:
        return 0.0

def to_int(v):
    try:
        if pd.isna(v): return 0
        val = float(v)
        if math.isnan(val): return 0
        return int(val)
    except:
        return 0

db_config = {
    "host": "localhost",
    "database": "kitapsatisdb",
    "user": "postgres",
    "password": db_password(),
    "port": "5432"
}

try:
    df = pd.read_excel('KİTAP BİLGİLERİ.xlsx', sheet_name='TAM KİTAPLAR')
    
    books_to_insert = []
    books_json = []

    def get_col_val(row, col_substr):
        for c in df.columns:
            # We must ignore case and whitespace differences
            c_clean = str(c).lower().replace('\n', '').replace(' ', '')
            substr_clean = col_substr.lower().replace(' ', '')
            if substr_clean in c_clean:
                return row[c]
        return None

    for _, row in df.iterrows():
        name = clean_value(get_col_val(row, 'kitapad'))
        if not name or str(name).lower() == 'nan':
            continue
            
        price = to_float(get_col_val(row, 'fiyat'))
        page_count = to_int(get_col_val(row, 'sayfa'))
        publisher = clean_value(get_col_val(row, 'yayın'))
        category = clean_value(get_col_val(row, 'bölüm'))
        language = clean_value(get_col_val(row, 'dil')) or "Türkçe"
        author = clean_value(get_col_val(row, 'yazar'))
        year = to_int(get_col_val(row, 'yıl')) or None
        
        # Edition should be string, sometimes it reads as a float (e.g. 1.0)
        edition_raw = get_col_val(row, 'baskı')
        if pd.isna(edition_raw):
            edition = ""
        else:
            if isinstance(edition_raw, float):
                edition = str(int(edition_raw))
            else:
                edition = str(edition_raw).strip()
                
        isbn = clean_value(get_col_val(row, 'isbn')) or ""
        stock = to_int(get_col_val(row, 'stok'))
        description = clean_value(get_col_val(row, 'açıklama'))
        
        image_url = ""
        
        book_obj = {
            "Name": name,
            "Price": price,
            "PageCount": page_count,
            "Publisher": publisher,
            "Category": category,
            "Language": language,
            "Author": author,
            "PublicationYear": year,
            "Edition": edition,
            "ISBN": isbn,
            "StockQuantity": stock,
            "Description": description,
            "IsActive": stock > 0,
            "IsFeatured": False,
            "MinStockLevel": 25,
            "ImageUrl": image_url
        }
        books_to_insert.append(book_obj)
        books_json.append(book_obj)

    with open('books_data_v2.json', 'w', encoding='utf-8') as f:
        json.dump(books_json, f, ensure_ascii=False, indent=2)
        
    print(f"Extracted {len(books_to_insert)} books from Excel.")

    # -----------------------------
    # DB Operations
    # -----------------------------
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    
    print("Truncating Books table (CASCADE)...")
    cur.execute('TRUNCATE TABLE "Books" RESTART IDENTITY CASCADE;')
    
    print("Inserting new records...")
    insert_query = '''
        INSERT INTO "Books" (
            "Name", "Price", "PageCount", "Publisher", "Category", 
            "Language", "Author", "PublicationYear", "Edition", 
            "ISBN", "StockQuantity", "Description", "IsActive", 
            "IsFeatured", "MinStockLevel", "ImageUrl"
        ) VALUES (
            %(Name)s, %(Price)s, %(PageCount)s, %(Publisher)s, %(Category)s,
            %(Language)s, %(Author)s, %(PublicationYear)s, %(Edition)s,
            %(ISBN)s, %(StockQuantity)s, %(Description)s, %(IsActive)s,
            %(IsFeatured)s, %(MinStockLevel)s, %(ImageUrl)s
        )
    '''
    
    for b in books_to_insert:
        cur.execute(insert_query, b)
        
    conn.commit()
    print(f"Inserted {len(books_to_insert)} books into the database successfully.")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals() and conn:
        cur.close()
        conn.close()
