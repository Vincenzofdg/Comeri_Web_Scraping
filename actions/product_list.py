import web_elements.product_list as element
from tools.selenium_functions import xpath
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from actions.product import product
from services.aws_get import request_aws_get as get

def product_list(url, client_id, category_id, browser):
    browser.get(url)
    client_products_on_db = get("product", client_id)

    try:
        accept_btn_div = xpath(element.pagination_div, browser)
        accept_btn_li = accept_btn_div.find_elements(By.TAG_NAME, "li")

        last_page_li =  xpath(f'{element.pagination_div}/li[{len(accept_btn_li) - 1}]', browser)
        number_of_pages = int(last_page_li.text)

        for page in range(number_of_pages):
            browser.get(f'{url}{page + 1}')

            cars_div = xpath(element.car_div, browser)
            car_page_qtd = int(len(cars_div.find_elements(By.XPATH, './div'))) - 2

            for car in range(car_page_qtd):
                img_from_div = xpath(f'{element.car_div}/div[{car + 1}]/div/div[1]/a', browser)
                img_from_div.click()

                product(client_id, category_id, client_products_on_db, browser)

                browser.back()

    except TimeoutException:
        print("TimeoutException problem on product")