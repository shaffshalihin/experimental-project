# conftest.py
import pytest
from selenium import webdriver

@pytest.fixture(scope="module")
def browser():
    # Setup: membuat instance browser
    driver = webdriver.Chrome()  # Anda bisa menggunakan WebDriver lain jika perlu
    yield driver  # Mengembalikan kontrol ke tes
    # Teardown: menutup browser setelah pengujian selesai
    driver.quit()
