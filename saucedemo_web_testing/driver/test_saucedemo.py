from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Ganti dengan path yang sesuai
# chromedriver_path = 'D:/shaff/kuliah/semester5/STQA/tugasTesting/driver/chromedriver.exe'

# Menginisialisasi service dan driver
# service = Service(chromedriver_path)
# driver = webdriver.Chrome(executable_path="D:/chromedriver.exe")

driver = webdriver.Chrome()


driver.implicitly_wait(10)
driver.maximize_window()

while True:

    driver.get("https://www.saucedemo.com/")

    # Menggunakan By untuk menemukan elemen
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

# print(driver.title)

# # Tutup dan quit driver
# driver.close()
# driver.quit()

# print("test completed")
