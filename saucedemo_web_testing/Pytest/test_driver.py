from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest

@pytest.fixture(scope="module")
def browser():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    yield driver
    # Teardown
    driver.quit()

def test_login_success(browser):
    # Find username and password fields and input values
    username = browser.find_element(By.ID, "user-name")
    password = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-button")

    # Enter valid credentials
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_button.click()

    # Assert that login is successful by checking URL or element on the next page
    assert "inventory.html" in browser.current_url

def test_login_failure(browser):
    # Refresh page for clean slate
    browser.refresh()

    # Enter invalid credentials
    username = browser.find_element(By.ID, "user-name")
    password = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "login-button")

    username.send_keys("invalid_user")
    password.send_keys("invalid_pass")
    login_button.click()

    # Check for error message
    error_message = browser.find_element(By.CSS_SELECTOR, ".error-message-container")
    assert "Epic sadface" in error_message.text
