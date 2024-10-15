from selenium import webdriver #untuk interaksi dengan web
from selenium.webdriver.common.by import By  # untuk selector pada html web
import pytest #untuk menggunakan fixture, parametrize
import time #untuk menghitung waktu
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#konfigurasi awal untuk interaksi dengan website
@pytest.fixture(scope="function")
def setup_driver():
    driver = webdriver.Chrome() #menggunakan browser chrome
    driver.get("https://www.saucedemo.com/") #membuka website
    driver.maximize_window() #membuka window ketika melakukan interaksi dengan website
    yield driver  # Mengembalikan driver ke test
    driver.quit()  # Teardown setelah test selesai


login_access = [
    ("standard_user", "secret_sauce"), #user valid
    ("locked_out_user", "secret_sauce"),#user locked
    ("problem_user", "secret_sauce"), #user bermasalah
    ("performance_glitch_user", "secret_sauce"), #user dengan performa yang menurun
    ("error_user", "secret_sauce"), #user error
    ("visual_user", "secret_sauce") #user dengan tampilan ui yang tidak sesuai
    ]

@pytest.mark.parametrize("username, password", login_access) #membuat parameter dengan acuan login_access yang akan digunakan berulang
def test_checkout(setup_driver, username, password): #pengujian melakukan checkout belanja
    driver = setup_driver #mengambil konfigurasi awal untuk digunakan sebagai driver

    #melakukan login dengan username dan password dari list login_access
    driver.find_element(By.ID, "user-name").send_keys(username) #mencari element dan mengirimkan value yang akan diisi
    driver.find_element(By.ID, "password").send_keys(password) #mencari element dan mengirimkan value yang akan diisi
    start_time_login = time.time() #menghitung waktu dimulai ketika mengklik button login
    driver.find_element(By.CLASS_NAME, "btn_action").click() #mengklik button login
    response_time_login = time.time() - start_time_login #menghitung selisih antara waktu sekarang dengan waktu start_time_login sebagai durasi response

    assert response_time_login < 1 #passed jika waktu response kurang dari 1 detik

    # Untuk pengguna yang valid, pastikan kita tidak melihat pesan kesalahan
    assert "inventory.html" in driver.current_url  # passed jika url mengandung string yang dimaksud

    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click() #menambahkan item ke cart
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click() #membuka cart

    assert "cart.html" in driver.current_url #passed jika url mengandung string yang dimaksud
    assert driver.find_element(By.CLASS_NAME, "cart_item").is_displayed() #passed jika cart item tampil di display

    driver.find_element(By.ID, "checkout").click() #mengklik button checkout

    assert "checkout-step-one.html" in driver.current_url #passed jika url mengandung string yang dimaksud

    driver.find_element(By.ID, "first-name").send_keys("arni") #mencari elemen dan mengirimkan value
    driver.find_element(By.ID, "last-name").send_keys("raihanah") #mencari elemen dan mengirimkan value
    driver.find_element(By.ID, "postal-code").send_keys("90214") #mencari elemen dan mengirimkan value
    driver.find_element(By.ID, "continue").click() #mengklik button continue

    assert "checkout-step-two.html" in driver.current_url #passed jika url mengandung string yang dimaksud

    driver.find_element(By.ID, "finish").click() #mengklik button finish 

    assert "checkout-complete.html" in driver.current_url #passed jika url mengandung string yang dimaksud

