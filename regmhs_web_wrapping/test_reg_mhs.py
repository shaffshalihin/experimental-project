from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

data = []
default_nim = "h071221"

def test_nim():
    for i in range(1, 51):
        try:
            driver = webdriver.Chrome()
            driver.get("https://regmhs.unhas.ac.id/")  # membuka website

            search_nim = default_nim + f"{i:03d}"
            
            # Klik menu "menu_spp_ukt"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "menu_spp_ukt"))
            ).click()

            # Pilih tahun akademik
            tahun_akademik = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tahun_akademik"))
            )
            select = Select(tahun_akademik)  # Menggunakan Select untuk elemen select
            select.select_by_value('20241')  # Misalnya '2021'

            # Isi NIM
            driver.find_element(By.ID, "nim").send_keys(search_nim)

            # Klik tombol "SearchTagihan"
            driver.find_element(By.ID, "SearchTagihan").click()

            # Tunggu dan ambil jumlah tagihan
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//td[@align="right"]/b'))
                )
                jumlah_tagihan = element.text
            except:
                jumlah_tagihan = "Tagihan tidak ditemukan"  # Jika gagal menemukan tagihan

            # Append NIM dan tagihan ke data
            data.append({
                'NIM': search_nim,
                'Jumlah Tagihan': jumlah_tagihan
            })

        except Exception as e:
            print(f"Terjadi kesalahan pada NIM {search_nim}: {e}")
            # Jika terjadi error (misalnya karena jaringan buruk), program akan melewati iterasi ini
            continue  # Lanjutkan ke NIM berikutnya

        finally:
            driver.quit()

    # Simpan ke Excel setelah loop selesai
    df = pd.DataFrame(data)
    df.to_excel('D:/shaff/kuliah/semester5/STQA/web_wrapping/hasil_tagihan.xlsx', index=False)
# Panggil fungsi untuk menjalankan tes
test_nim()
