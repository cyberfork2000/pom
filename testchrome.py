import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from hamcrest import assert_that, equal_to
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://localhost'
REGISTER_URL = BASE_URL + '/register'
REGISTER_URL_SUCCESS = BASE_URL + '/account-activation/activate'
LOGIN_URL = BASE_URL + '/signin'


class BasePage(object):

    def __init__(self, driver):
        self._driver = driver


class RegisterPageLocators(object):

    ELEMENT_IDS = {
        "FIELDS": {
            "NAME": 'name',
            "COMPANY": 'workplace',
            "EMAIL": 'email',
            "PASSWORD": 'password'
        },
        "ACCEPT_BUTTONS": {
            "NAME": '.MuiFormControl-root:nth-child(1) .MuiSvgIcon-root',
            "COMPANY": '.MuiFormControl-root:nth-child(2) .MuiSvgIcon-root',
            "EMAIL": '.MuiFormControl-root:nth-child(3) .MuiSvgIcon-root',
            "PASSWORD": '.MuiFormControl-root:nth-child(4) .MuiSvgIcon-root'
        },
        "REGISTER_SUCCESS": {
            "SUCCESS": 'aaaa'
        },
        "BUTTON": 'sign-up-button'
    }


class RegisterPage(BasePage):

    def it_exists(self, id):
        elements = self._driver.find_elements_by_id(id)
        if elements:
            return elements[0]
        else:
            return False

    def navigate_to_register_page(self):
        self._driver.get(REGISTER_URL)
        time.sleep(2)

    def set_name(self, name):
        field = self.it_exists(RegisterPageLocators.ELEMENT_IDS["FIELDS"]["NAME"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def set_company(self, name):
        field = self.it_exists(RegisterPageLocators.ELEMENT_IDS["FIELDS"]["COMPANY"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def set_email(self, name):
        field = self.it_exists(RegisterPageLocators.ELEMENT_IDS["FIELDS"]["EMAIL"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def set_password(self, name):
        field = self.it_exists(RegisterPageLocators.ELEMENT_IDS["FIELDS"]["PASSWORD"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def new_user_is_accepted(self, expected_url=REGISTER_URL_SUCCESS):
        button = self.it_exists(RegisterPageLocators.ELEMENT_IDS["BUTTON"])
        assert_that(button.is_displayed(), equal_to(True))
        assert_that(button.is_enabled(), equal_to(True))
        print(self._driver.title)
        button.click()
        print("submitted")
        time.sleep(3)
        WebDriverWait(self._driver, 15).until(EC.url_changes(expected_url))
        assert self._driver.page_source.find("Activate your account")


class LoginPage(BasePage):

    def user_login(self):
        self._driver.get(LOGIN_URL)
        time.sleep(2)

    def check_login(self):
        print(self._driver.title)


class TestTemplate(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


class TestRegisterPage(TestTemplate):

    def test_register_page(self):
        register_page = RegisterPage(self.driver)
        register_page.navigate_to_register_page()
        register_page.set_name("Luna Landing")
        register_page.set_company("Pie")
        register_page.set_email("fff@ffff.com")
        register_page.set_password("1Password")
        register_page.new_user_is_accepted()


if __name__ == '__main__':
    unittest.main()
