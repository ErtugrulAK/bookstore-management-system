import psycopg2
import os
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

def update_images():
    conn_str = f"host=localhost port=5432 dbname=kitapsatisdb user=postgres password={db_password()}"
    
    manual_matches = {
        "bilgisayarprogramlama": "bilisayarprogramlamamatlabuygulamali",
        "endustriyelatiksularinyonetimi": "endustriyelatiksularinyonetilmesi",
        "frenchforengineers": "fransizca",
        "fiziklaboratuvariiideneykitapcigi": "fiziklabii",
        "giysikalipciligii": "giysikalipci1",
        "insaatmuhendisleriicinmalzemebilgisi": "malzemebilgisiinsmuhicin",
        "isletmeyonetimiveorganizasyonu": "isletmeyontemiveorganizasyonu",
        "jeofiziktesinyalanalizi": "jeofiziksinyalanalizi",
        "katiatiktoplamatasimavebertarafsistemlerinineniyilenmesiveekonomisi": "katiatiktoplamatasbertarafsis",
        "kilmineralleri": "kilmineralleridersnotlari",
        "kim1016organikkimyauygulamadeneyleri": "genelkimyaicinlabdeneyleri",
        "kimyalaboratuvarideneyleri": "genelkimyaicinlabdeneylerikitap",
        "madenlerdesuaritimivepompalar": "madenlerdesuatimivepompalar",
        "matematikiilineercebir": "matematikilineercebir",
        "potansiyelteorivejeofizikuygulamalari": "potansiyelteorijeofizikuygulamalari",
        "sukaynaklarininkiyilestirilmesi": "sukaynaklarinigelistirilmesi",
        "sukuvvetisuyapilari": "sukuvvetisuyapilariciltix",
        "sukuvvetitesislerindesayisalornekler": "sukuvvetitessayisalornekle",
        "turkdevrimtarihii": "turkdevrimtarihi",
        "uretimplanama": "uretimplanlama",
        "mineraloji": "minerolojigenelminerolojicilti",
        "yeraltimadenmakineleriivemekanizasyonu": "yeraltimadenmakinalarivemekanizasyonu",
        "cevremuhendiligindemikrobiyolojikuygulamalar": "cevremuhendisligindemikrobiyolojikuygulamalar",
        "cevreuhendisligindebiyoprosesler": "cevremuhendisligindebiyoprosesler",
        "izmirinkurtulusuveyuzbasiserafettin": "insakilik",
        "aktifcamursurecinintasarimuygulamalaricilti": "atiksuaritmasistemlerinintasarimesaslarici",
        "aktifcamursurecinintasarimuygulamalariciltii": "atiksuaritmasistemlerinintasarimesaslaricii",
        "madenjeolojisiuygulamaklavuzu": "madenjeolojisiuygulamakilavuzu",
    }

    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        cur.execute('SELECT "Id", "Name" FROM "Books"')
        db_books = cur.fetchall()
        
        files = os.listdir(img_dir)
        updated_count = 0
        
        for filename in files:
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
                
            img_name_only = os.path.splitext(filename)[0]
            norm_img = normalize(img_name_only)
            image_url = f"/images/books/{filename}"
            
            matched_id = None
            
            # 1. Try exact normalized match
            for book_id, book_name in db_books:
                norm_db = normalize(book_name)
                if norm_db == norm_img:
                    matched_id = book_id
                    break
            
            # 2. Try manual matches
            if not matched_id and norm_img in manual_matches:
                target_norm_db = manual_matches[norm_img]
                for book_id, book_name in db_books:
                    if normalize(book_name) == target_norm_db:
                        matched_id = book_id
                        break
            
            # 3. Try "starts with" or "contains"
            if not matched_id:
                for book_id, book_name in db_books:
                    norm_db = normalize(book_name)
                    if (len(norm_img) > 5 and norm_img in norm_db) or (len(norm_db) > 5 and norm_db in norm_img):
                        matched_id = book_id
                        break

            if matched_id:
                cur.execute('UPDATE "Books" SET "ImageUrl" = %s WHERE "Id" = %s', (image_url, matched_id))
                # print(f"Matched: {img_name_only} -> {image_url}")
                updated_count += 1
            else:
                print(f"FAILED: {img_name_only}")
        
        conn.commit()
        print(f"Total updated: {updated_count}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals(): cur.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    update_images()
