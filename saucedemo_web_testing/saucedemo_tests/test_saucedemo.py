from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
from selenium.common.exceptions import NoSuchElementException

# Inisialisasi driver
@pytest.fixture(scope="module")
def setup_driver():
    driver = webdriver.Chrome()
    driver.minimize_window()
    yield driver
    driver.quit()  # Menutup browser setelah pengujian selesai

# Data akses login
login_access = [
    ("standard_user", "secret_sauce"),  # Pengguna valid
    ("locked_out_user", "secret_sauce"),  # Pengguna terkunci
    ("invalid_user", "secret_sauce")  # Pengguna tidak valid
]

@pytest.mark.parametrize("username, password", login_access)
def test_login(setup_driver, username, password):
    driver = setup_driver  # Mendapatkan driver dari fixture
    driver.get("https://www.saucedemo.com/")
    
    # Mencari elemen input
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CLASS_NAME, "btn_action")

    # Mengisi input dan menekan tombol login
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    # Memeriksa hasil login
    if username == "standard_user":
        # Untuk pengguna yang valid
        assert "Swag Labs" in driver.title  # Pastikan halaman yang tepat dimuat
        assert driver.find_element(By.CLASS_NAME, "product_label")  # Memastikan elemen produk muncul
    elif username == "locked_out_user":
        # Untuk pengguna terkunci
        try:
            invalid_text = driver.find_element(By.CSS_SELECTOR, ".error-message-container.error").text
            assert invalid_text == "Epic sadface: Sorry, this user has been locked out."  # Pesan kesalahan yang benar
        except NoSuchElementException:
            assert False, "Error message not displayed for locked out user."
    else:
        # Untuk pengguna yang tidak valid
        try:
            invalid_text = driver.find_element(By.CSS_SELECTOR, ".error-message-container.error").text
            assert invalid_text == "Epic sadface: Username and password do not match any user in this service"  # Pesan kesalahan untuk pengguna tidak valid
        except NoSuchElementException:
            assert False, "Error message not displayed for invalid user."

def test_product_page(setup_driver):
    driver = setup_driver
    driver.get("https://www.saucedemo.com/")
    
    # Login sebagai pengguna valid
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.CLASS_NAME, "btn_action").click()

    # Memeriksa halaman produk
    assert "Swag Labs" in driver.title
    assert driver.find_element(By.CLASS_NAME, "inventory_list")  # Memastikan daftar produk ada

    # Memilih produk pertama
    driver.find_element(By.CLASS_NAME, "inventory_item").click()

    # Memeriksa detail produk
    assert driver.find_element(By.CLASS_NAME, "inventory_details_name").is_displayed()  # Nama produk
    assert driver.find_element(By.CLASS_NAME, "inventory_details_desc").is_displayed()  # Deskripsi produk
    assert driver.find_element(By.CLASS_NAME, "inventory_details_price").is_displayed()  # Harga produk

def test_logout(setup_driver):
    driver = setup_driver
    driver.get("https://www.saucedemo.com/")
    
    # Login sebagai pengguna valid
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.CLASS_NAME, "btn_action").click()

    # Memeriksa bahwa pengguna sudah login
    assert "Swag Labs" in driver.title

    # Melakukan logout
    driver.find_element(By.ID, "react-burger-menu-btn").click()  # Klik tombol menu
    driver.find_element(By.ID, "logout_sidebar_link").click()  # Klik link logout

    # Memeriksa bahwa halaman login muncul setelah logout
    assert "Swag Labs" not in driver.title  # Judul tidak boleh mengandung "Swag Labs"
    assert driver.find_element(By.ID, "user-name")  # Memastikan elemen input username ada

