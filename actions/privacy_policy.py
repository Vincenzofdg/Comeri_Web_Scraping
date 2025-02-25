from tools.selenium_functions import xpath
from web_elements.privacy_policy import policy_btn
from selenium.common.exceptions import TimeoutException


def privacy_policy(url, browser):
    browser.get(url)

    try:
        accept_btn = xpath(policy_btn, browser)
        accept_btn.click()

    except TimeoutException:
        print("TimeoutException problem, on file: action/privacy_policy.py")
        