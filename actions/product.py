import json
import web_elements.product as element
import datetime
from tools.id_generator import id_generator, hash_generator
from tools.selenium_functions import xpath
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

from services.aws_post import request_aws_post as post


def product(client_id, category_id, products_on_db, current_product_list, browser):
    id_form_scrapping_site = browser.current_url.split('-')[-1]
    pictures = []
    description = ""
    now_utc = datetime.datetime.now()
    data_formated = now_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    obj_to_inject = {
        "id": id_form_scrapping_site,
        "categoryId": category_id,
        "emporiumId": client_id,
        "name": "",
        "nameSearch": "",
        "value": 0.0,
        "highlighted": False,
        "available": True,
        "description": "",
        "reference": hash_generator(),
        "discount": 0.0,
        "discountType": "currency",
        "galleryPath": "",
        "highlightedGalleryPath": "bot-auto",
        "videoPath": "",
        "createdAt": data_formated,
        "updatedAt": data_formated,
        "__typename": "Products"
    }

    try:
        product_brand = xpath(element.brand_h1, browser).text
        product_tile = xpath(element.title_h1, browser).text

        is_name_on_db = [obj for obj in products_on_db if obj["id"] == id_form_scrapping_site and obj["categoryId"] == category_id]

        if len(is_name_on_db) >= 1:
            print(f"\n[UPDATE]\nID: {is_name_on_db[0]["id"]}\nNAME: {is_name_on_db[0]["name"]}")

            obj_to_inject["id"] = is_name_on_db[0]["id"]
            obj_to_inject["reference"] = is_name_on_db[0]["reference"]
            obj_to_inject["videoPath"] = f"emporiums/videos/{client_id}/{is_name_on_db[0]["id"]}/preview.mp4"
        else:
            # print(f"\n[CREATE]\nID: {is_name_on_db[0]["id"]}\nNAME: {is_name_on_db[0]["name"]}")
            print(f"CRIANDO NOVO")

        obj_to_inject["name"] = f"{product_brand} - {product_tile}"
        obj_to_inject["nameSearch"] = product_tile.replace(" ", "_").replace(".", "_").replace("-", "_").upper()

        # Product Description
        features_with_image_container = xpath(element.type_with_img_container, browser)
        features_with_image = features_with_image_container.find_elements(By.TAG_NAME, "span")

        for i, feature in enumerate(features_with_image):
            if i % 2 == 0:
                description += f"* {feature.text.replace("Â", "â").replace("M", "m").replace("Í", "í").replace("V", "v")} {features_with_image[i + 1].text}\n\n"

        description += "------------------\n\n"

        product_accessories_title = xpath(element.product_acessories_title, browser).text
        description += f"{product_accessories_title}:\n\n"

        product_accessories_container = xpath(element.product_acessories, browser)
        product_accessories = product_accessories_container.find_elements(By.TAG_NAME, "p")

        for feature in product_accessories:
            description += f"* {feature.text}\n\n"

        try:
                see_more_btn = xpath(element.see_more_btn, browser)
                see_more_btn.click()

                product_accessories_more_container = xpath(element.product_acessories_more, browser)
                product_accessories_more = product_accessories_more_container.find_elements(By.TAG_NAME, "p")

                for feature in product_accessories_more:
                    description += f"* {feature.text}\n\n"

        except NoSuchElementException:
            pass
        finally:
            description += "------------------\n\n"

        main_details_title = xpath(element.main_details_title, browser).text
        description += f"{main_details_title}:\n\n"

        main_details = xpath(element.main_details, browser).text
        description += main_details

        pictures_container = xpath(element.picture_container, browser)
        img_url_elements = pictures_container.find_elements(By.TAG_NAME, "img")

        for img_url in img_url_elements:
            url = img_url.get_attribute("src")
            pictures.append(url)

        obj_to_inject["galleryPath"] = json.dumps(pictures)

        try:
            promotion_value = browser.find_element(By.XPATH, element.promotion_p).text[7:].replace(".", "").replace(",", ".")
            full_price_value = browser.find_element(By.XPATH, element.full_price_p).text[6:].replace(".", "").replace(",", ".")
            discount = round(float(full_price_value) - float(promotion_value), 2)

            obj_to_inject["discount"] = discount
            obj_to_inject["value"] = float(full_price_value)
        except NoSuchElementException:
            product_value = xpath(element.price_p, browser).text
            obj_to_inject["value"] = float(product_value[3:].replace(".", "").replace(",", "."))

        obj_to_inject["description"] = description

        current_product_list.append(obj_to_inject)
        post("product", data=obj_to_inject)

    except TimeoutException:
        product_brand = xpath(element.brand_h1, browser).text
        product_tile = xpath(element.title_h1, browser).text

        is_name_on_db = [obj for obj in products_on_db if obj["id"] == id_form_scrapping_site and obj["categoryId"] == category_id]

        if len(is_name_on_db) >= 1:
            print(f"\n[UPDATE]\nID: {is_name_on_db[0]["id"]}\nNAME: {is_name_on_db[0]["name"]}")

            obj_to_inject["id"] = is_name_on_db[0]["id"]
            obj_to_inject["reference"] = is_name_on_db[0]["reference"]
            obj_to_inject["videoPath"] = f"emporiums/videos/{client_id}/{is_name_on_db[0]["id"]}/preview.mp4"
        else:
            # print(f"\n[CREATE]\nID: {is_name_on_db[0]["id"]}\nNAME: {is_name_on_db[0]["name"]}")
            print(f"CRIANDO NOVO")

        obj_to_inject["name"] = f"{product_brand} - {product_tile}"
        obj_to_inject["nameSearch"] = product_tile.replace(" ", "_").replace(".", "_").replace("-", "_").upper()

        # Product Description
        features_with_image_container = xpath(element.type_with_img_container, browser)
        features_with_image = features_with_image_container.find_elements(By.TAG_NAME, "span")

        for i, feature in enumerate(features_with_image):
            if i % 2 == 0:
                description += f"* {feature.text.replace("Â", "â").replace("M", "m")} {features_with_image[i + 1].text}\n\n"

        description += "------------------\n\n"

        product_accessories_title = xpath(element.product_acessories_title, browser).text
        description += f"{product_accessories_title}:\n\n"

        product_accessories_container = xpath("/html/body/main/div/div[3]/div/div/div/div/div", browser)
        product_accessories = product_accessories_container.find_elements(By.TAG_NAME, "p")

        for feature in product_accessories:
            description += f"* {feature.text}\n\n"

        description += "------------------\n\n"


        main_details_title = xpath(element.main_details_title, browser).text
        description += f"{main_details_title}:\n\n"

        main_details = xpath(element.main_details, browser).text
        description += main_details

        pictures_container = xpath(element.picture_container, browser)
        img_url_elements = pictures_container.find_elements(By.TAG_NAME, "img")

        for img_url in img_url_elements:
            url = img_url.get_attribute("src")
            pictures.append(url)

        obj_to_inject["galleryPath"] = json.dumps(pictures)

        try:
            promotion_value = browser.find_element(By.XPATH, element.promotion_p).text[7:].replace(".", "").replace(",",
                                                                                                                    ".")
            full_price_value = browser.find_element(By.XPATH, element.full_price_p).text[6:].replace(".", "").replace(
                ",", ".")
            discount = round(float(full_price_value) - float(promotion_value), 2)

            obj_to_inject["discount"] = discount
            obj_to_inject["value"] = float(full_price_value)
        except NoSuchElementException:
            product_value = xpath(element.price_p, browser).text
            obj_to_inject["value"] = float(product_value[3:].replace(".", "").replace(",", "."))

        obj_to_inject["description"] = description

        current_product_list.append(obj_to_inject)
        post("product", data=obj_to_inject)
