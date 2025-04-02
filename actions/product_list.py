import web_elements.product_list as element
from tools.selenium_functions import xpath
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from actions.product import product
from services.aws_delete import request_aws_delete as delete_by_id

def product_list(url, client_id, category_id, current_products, browser):
    current_product_list = []
    browser.get(url)

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

                product(client_id, category_id, current_products, current_product_list, browser)

                browser.back()

        product_diff = [product for product in current_products
                        if product["name"] not in {p["name"] for p in current_product_list}]

        for product_delete in product_diff:
            delete_by_id("product", product_delete["id"])
            print(f"\n[DELETE]\nID: {product_delete["id"]}\nNAME: {product_delete["name"]}")

    except TimeoutException:
        cars_div = xpath(element.car_div, browser)
        car_page_qtd = int(len(cars_div.find_elements(By.XPATH, './div'))) - 2

        for car in range(car_page_qtd):
            print(f"[Página 1] {car_page_qtd} / {car + 1}")

            img_from_div = xpath(f'{element.car_div}/div[{car + 1}]/div/div[1]/a', browser)
            img_from_div.click()

            product(client_id, category_id, current_products, current_product_list, browser)

            browser.back()


        product_diff = [product for product in current_products
                        if product["name"] not in {p["name"] for p in current_product_list}]

        for product_delete in product_diff:
            delete_by_id("product", product_delete["id"])
            print(f"\n[DELETE]\nID: {product_delete["id"]}\nNAME: {product_delete["name"]}")