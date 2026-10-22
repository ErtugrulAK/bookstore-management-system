import subprocess
import time
import os
import sys
import psycopg2
from pg_env import db_password, admin_ui_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def print_flush(msg):
    print(msg)
    sys.stdout.flush()

def kill_ports():
    print_flush("Checking and cleaning up ports 5229 and 5173...")
    for port in ["5229", "5173"]:
        try:
            output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode('utf-8', errors='ignore')
            lines = output.strip().split('\n')
            pids = set()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    pids.add(pid)
            for pid in pids:
                if pid != "0":
                    print_flush(f"Killing process {pid} using port {port}...")
                    subprocess.call(f"taskkill /F /PID {pid}", shell=True)
        except Exception:
            pass

def clean_database_for_user():
    print_flush("Cleaning up database for user a@a (UserId=4) to ensure deterministic flow...")
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
        
        # 1. Delete user addresses to force address form to show up
        cur.execute('DELETE FROM "UserAddresses" WHERE "UserId" = 4;')
        print_flush("Deleted user addresses.")
        
        # 2. Clean existing cart items (OrderItems where Order is Pending/Status=0)
        cur.execute('DELETE FROM "OrderItems" WHERE "OrderId" IN (SELECT "Id" FROM "Orders" WHERE "UserId" = 4 AND "Status" = 0);')
        print_flush("Deleted cart order items.")
        
        # 3. Delete pending cart order
        cur.execute('DELETE FROM "Orders" WHERE "UserId" = 4 AND "Status" = 0;')
        print_flush("Deleted cart orders.")
        
        conn.commit()
        print_flush("Database committed successfully.")
    except Exception as e:
        print_flush(f"Error cleaning database: {e}")
    finally:
        if 'conn' in locals() and conn:
            cur.close()
            conn.close()

def set_react_input(driver, element, value):
    driver.execute_script("""
        var setValue = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setValue.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, element, value)

def set_react_textarea(driver, element, value):
    driver.execute_script("""
        var setValue = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setValue.call(arguments[0], arguments[1]);
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, element, value)

def main():
    # Make sure ports are free
    kill_ports()
    
    # Clean DB
    clean_database_for_user()
    
    print_flush("Starting backend API...")
    api_process = subprocess.Popen(
        ["dotnet", "run", "--project", "BookStore.Api"], 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL
    )
    
    print_flush("Starting frontend Web app...")
    web_process = subprocess.Popen(
        ["npm", "run", "dev"], 
        cwd="BookStore.Web", 
        stdout=subprocess.DEVNULL, 
        stderr=subprocess.DEVNULL, 
        shell=True
    )
    
    print_flush("Waiting 15 seconds for servers to initialize...")
    time.sleep(15)
    
    driver = None
    try:
        print_flush("Launching headless browser...")
        try:
            options = EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1280,960")
            options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Edge(options=options)
            print_flush("Edge loaded successfully.")
        except Exception as e:
            print_flush(f"Edge failed. Trying Chrome... Error: {e}")
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1280,960")
            options.add_argument("--ignore-certificate-errors")
            options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            driver = webdriver.Chrome(options=options)
            print_flush("Chrome loaded successfully.")
            
        os.makedirs("manual_assets", exist_ok=True)
        
        # 1. Login page
        print_flush("Navigating to login page...")
        driver.get("http://localhost:5173/login")
        
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='E-posta veya Kullanıcı Adı']"))
        )
        
        print_flush("Typing login details...")
        set_react_input(driver, username_input, "a@a")
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Şifre']")
        set_react_input(driver, password_input, admin_ui_password())
        
        time.sleep(1.5)
        driver.save_screenshot("manual_assets/01_login.png")
        print_flush("Saved 01_login.png")
        
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit' or contains(text(), 'Giriş')]")
        submit_btn.click()
        
        time.sleep(4) # Wait for login and home redirection
        
        # 1.1 Compliance: Distance Sales Agreement
        print_flush("Navigating to Distance Sales page...")
        driver.get("http://localhost:5173/mesafeli-satis")
        time.sleep(2)
        driver.save_screenshot("manual_assets/07_distance_sales.png")
        print_flush("Saved 07_distance_sales.png")
        
        # 1.2 Compliance: Contact/Merchant Info
        print_flush("Navigating to Contact page...")
        driver.get("http://localhost:5173/iletisim")
        time.sleep(2)
        driver.save_screenshot("manual_assets/08_contact.png")
        print_flush("Saved 08_contact.png")
        
        # 2. Home page & add book
        print_flush("Navigating to home page...")
        driver.get("http://localhost:5173/")
        time.sleep(4)
        
        driver.save_screenshot("manual_assets/02_home.png")
        print_flush("Saved 02_home.png")
        
        print_flush("Adding book to cart...")
        add_to_cart_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-btn"))
        )
        driver.execute_script("arguments[0].click();", add_to_cart_btn)
        time.sleep(3) # Wait for toast and add cart animation
        
        # 3. Cart Step 1 (Sepetim)
        print_flush("Navigating to cart page...")
        driver.get("http://localhost:5173/sepet")
        time.sleep(4)
        
        driver.save_screenshot("manual_assets/03_cart_step1.png")
        print_flush("Saved 03_cart_step1.png")
        
        # Click "Sepeti Onayla"
        print_flush("Proceeding to delivery info...")
        confirm_btn = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Sepeti Onayla')]"))
        )
        driver.execute_script("arguments[0].click();", confirm_btn)
        time.sleep(4)
        
        # 4. Cart Step 2 (Bilgiler - Delivery Info)
        print_flush("Filling delivery information...")
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchable-select-trigger"))
        )
        
        # SearchableSelect for City (İl)
        print_flush("Selecting city...")
        city_select = driver.find_elements(By.CLASS_NAME, "searchable-select-trigger")[0]
        driver.execute_script("arguments[0].click();", city_select)
        
        city_search = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ara...']"))
        )
        set_react_input(driver, city_search, "İzmir")
        time.sleep(1)
        city_option = driver.find_element(By.XPATH, "//div[contains(@class, 'option-item') and contains(text(), 'İzmir')]")
        driver.execute_script("arguments[0].click();", city_option)
        time.sleep(2)
        
        # SearchableSelect for District (İlçe)
        print_flush("Selecting district...")
        district_select = driver.find_elements(By.CLASS_NAME, "searchable-select-trigger")[1]
        driver.execute_script("arguments[0].click();", district_select)
        
        district_search = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Ara...']"))
        )
        set_react_input(driver, district_search, "Bornova")
        time.sleep(1)
        district_option = driver.find_element(By.XPATH, "//div[contains(@class, 'option-item') and contains(text(), 'Bornova')]")
        driver.execute_script("arguments[0].click();", district_option)
        time.sleep(2)
        
        # Now type the text details
        print_flush("Typing text details...")
        ad_input = driver.find_element(By.XPATH, "//input[@name='ad']")
        set_react_input(driver, ad_input, "Ahmet")
        
        soyad_input = driver.find_element(By.XPATH, "//input[@name='soyad']")
        set_react_input(driver, soyad_input, "Yılmaz")
        
        adres_input = driver.find_element(By.XPATH, "//textarea[@name='adres']")
        set_react_textarea(driver, adres_input, "Ege Üniversitesi Kampüsü Lojmanları, No: 15")
        
        telefon_input = driver.find_element(By.XPATH, "//input[@name='telefon']")
        set_react_input(driver, telefon_input, "0555 555 55 55")
        time.sleep(2)
        
        driver.save_screenshot("manual_assets/04_cart_step2.png")
        print_flush("Saved 04_cart_step2.png")
        
        # Click "Ödeme Adımına Geç"
        next_step_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Ödeme Adımına Geç')]")
        driver.execute_script("arguments[0].click();", next_step_btn)
        time.sleep(4)
        
        # 5. Cart Step 3 (Ödeme - Payment Info)
        print_flush("Filling payment information...")
        
        kart_isim = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='kartIsim']"))
        )
        set_react_input(driver, kart_isim, "Ahmet Yılmaz")
        
        kart_no = driver.find_element(By.XPATH, "//input[@name='kartNo']")
        set_react_input(driver, kart_no, "4355 1234 5678 9012")
        
        kart_skt = driver.find_element(By.XPATH, "//input[@name='kartSkt']")
        set_react_input(driver, kart_skt, "12 / 28")
        
        kart_cvv = driver.find_element(By.XPATH, "//input[@name='kartCvv']")
        set_react_input(driver, kart_cvv, "321")
        time.sleep(2)
        
        driver.save_screenshot("manual_assets/05_cart_step3.png")
        print_flush("Saved 05_cart_step3.png")
        
        # Click "Siparişi Onayla"
        print_flush("Completing purchase...")
        complete_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Siparişi Onayla')]")
        driver.execute_script("arguments[0].click();", complete_btn)
        time.sleep(6) # Wait for backend order completion and redirection to success page
        
        # 6. Cart Step 4 (Onay - Order confirmation)
        print_flush("Capturing order confirmation page...")
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "success-container"))
        )
        time.sleep(2)
        driver.save_screenshot("manual_assets/06_cart_step4.png")
        print_flush("Saved 06_cart_step4.png")
        
        print_flush("All screenshots captured successfully!")
        
    except Exception as err:
        print_flush(f"Error during browser automation: {err}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        
        print_flush("Stopping background servers...")
        api_process.terminate()
        web_process.terminate()
        kill_ports()
        print_flush("Done.")

if __name__ == "__main__":
    main()
