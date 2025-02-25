from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from dotenv import dotenv_values
from actions.privacy_policy import privacy_policy
from actions.product_list import product_list
from time import sleep

# Browser Settings
setting = Options()
setting.add_argument("--disable-extensions")
setting.add_argument("--disable-gpu")
setting.add_argument("--no-sandbox")
setting.add_argument("--disable-dev-shm-usage")
setting.add_argument("--headless")

browser = webdriver.Firefox(options=setting)
# browser = webdriver.Firefox()

env = dotenv_values(".env")
url = env["url"]
url_used_cars = env["url_used_cars"]
url_new_cars = env["url_new_cars"]

client_id = env["client_id"]
used_car_category_id = env["used_car_category_id"]
new_car_category_id = env["new_car_category_id"]


try:
    # Accept Privacy Policy
    try:
        privacy_policy(url, browser)
    except ElementNotInteractableException:
        pass

    # Scrap Used Cars
    product_list(url_used_cars, client_id, used_car_category_id, browser)

    # Scrap New Cars
    # product_list(url_new_cars, client_id, new_car_category_id, browser)
except TimeoutException:
    print("error")
    pass
finally:
    browser.close()