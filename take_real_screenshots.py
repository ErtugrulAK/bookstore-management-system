import subprocess
import time
import os
import sys
from pg_env import admin_ui_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

def kill_ports():
    print("Checking and cleaning up ports 5229 and 5173...")
    # Clean up port 5229 and 5173 on Windows if they are occupied
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
                    print(f"Killing process {pid} using port {port}...")
                    subprocess.call(f"taskkill /F /PID {pid}", shell=True)
        except Exception:
            pass

def main():
    # Make sure ports are free before we start
    kill_ports()
    
    print("Starting backend API...")
    api_process = subprocess.Popen(
        ["dotnet", "run", "--project", "BookStore.Api"], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    print("Starting frontend Web app...")
    web_process = subprocess.Popen(
        ["npm", "run", "dev"], 
        cwd="BookStore.Web", 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        shell=True
    )
    
    print("Waiting 12 seconds for servers to initialize...")
    time.sleep(12)
    
    driver = None
    try:
        print("Launching headless browser...")
        # Try Microsoft Edge first since it is built-in on Windows
        try:
            options = EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1280,960")
            options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Edge(options=options)
            print("Edge loaded successfully.")
        except Exception as e:
            print("Edge failed. Trying Chrome...", e)
            options = ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--window-size=1280,960")
            options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Chrome(options=options)
            print("Chrome loaded successfully.")
            
        # Navigate to login page
        print("Navigating to login page...")
        driver.get("http://localhost:5173/login")
        
        # Wait for username input
        username_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='E-posta veya Kullanıcı Adı']"))
        )
        
        # Enter credentials
        print("Logging in...")
        username_input.send_keys("admin")
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Şifre']")
        password_input.send_keys(admin_ui_password())
        
        submit_btn = driver.find_element(By.XPATH, "//button[type='submit' or contains(text(), 'Giriş')]")
        submit_btn.click()
        
        # Wait a moment for login to complete and token to be saved
        time.sleep(3)
        
        # Navigate directly to admin panel
        print("Navigating to Admin panel...")
        driver.get("http://localhost:5173/admin")
        
        # Wait for admin layout to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "admin-layout"))
        )
        
        # Ensure manual_assets folder exists
        os.makedirs("manual_assets", exist_ok=True)
        time.sleep(2)  # Wait for any data fetching/charts animation to settle
        
        # 1. Capture Dashboard tab (active by default)
        print("Capturing Dashboard...")
        driver.save_screenshot("manual_assets/dashboard_mockup.png")
        print("Saved dashboard_mockup.png")
        
        # 2. Capture Books tab
        print("Navigating to Books tab...")
        books_btn = driver.find_element(By.XPATH, "//button[contains(., 'Kitaplar')]")
        books_btn.click()
        time.sleep(2)
        driver.save_screenshot("manual_assets/books_mockup.png")
        print("Saved books_mockup.png")
        
        # 3. Capture Orders tab
        print("Navigating to Orders tab...")
        orders_btn = driver.find_element(By.XPATH, "//button[contains(., 'Siparişler')]")
        orders_btn.click()
        time.sleep(2)
        driver.save_screenshot("manual_assets/orders_mockup.png")
        print("Saved orders_mockup.png")
        
        # 4. Capture Detailed Report tab
        print("Navigating back to Panel...")
        panel_btn = driver.find_element(By.XPATH, "//button[contains(., 'Panel')]")
        panel_btn.click()
        time.sleep(1)
        
        print("Navigating to Detailed Report tab...")
        report_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Detaylı Rapor')]")
        report_btn.click()
        time.sleep(2)
        driver.save_screenshot("manual_assets/reports_mockup.png")
        print("Saved reports_mockup.png")
        
        print("All screenshots captured successfully!")
        
    except Exception as err:
        print(f"Error during browser automation: {err}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
        
        print("Stopping background servers...")
        api_process.terminate()
        web_process.terminate()
        kill_ports()
        print("Done.")

if __name__ == "__main__":
    main()
