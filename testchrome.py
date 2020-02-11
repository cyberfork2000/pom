import time
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from hamcrest import assert_that, equal_to
import string
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = 'http://localhost'
REGISTER_URL = BASE_URL + '/register'
REGISTER_URL_SUCCESS = BASE_URL + '/account-activation/activate'
LOGIN_URL = BASE_URL + '/signin'
DOCKS_URL = BASE_URL + '/docks'
whoami = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))


class BasePage(object):

    def __init__(self, driver):
        self._driver = driver


class DockPageLocators(object):

    ELEMENT_IDS = {
        "XPATH": {
            "ADD_DOCK_POPUP": '//div[@role="presentation"]/section',
            "LOGOUT_BUTTON": '//div[@title="Logout"]',
            "DOCKS_BUTTON": '//div[@title="Docks"]',
            "LOBBY_BUTTON": '//div[@title="Lobby Dashboard"]'
        },
        "CSS": {
            "ADD_DOCK_BUTTON": 'button.MuiButtonBase-root.MuiButton-root',
        },
        "ID": {
            "DOCK_ID_FIELD": 'id',
            "CUSTOM_ID_FIELD": 'customId',
            "BUILDING_FIELD": 'building',
            "BUILDING_MENU": 'menu-building',
            "FLOOR_FIELD": 'floor',
            "FLOOR_MENU": 'menu-floor',
            "AREA_FIELD": 'area',
            "AREA_MENU": 'menu-area',
            "ADD_DOCK_CANCEL_BUTTON": 'cancel-btn',
        }
    }


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
        "RESEND": 'resend-email-button',
        "BUTTON": 'sign-up-button'
    }


class LoginPageLocators(object):

    ELEMENT_IDS = {
        "FIELDS": {
            "EMAIL": 'email',
            "PASSWORD": 'password'
        },
        "BUTTON": 'login-button'
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

    def new_user_is_accepted(self):
        button = self.it_exists(RegisterPageLocators.ELEMENT_IDS["BUTTON"])
        assert_that(button.is_displayed(), equal_to(True))
        assert_that(button.is_enabled(), equal_to(True))
        button.click()
        print("registered")
        time.sleep(3)
        assert self._driver.page_source.find("Activate your account")


class LoginPage(BasePage):

    def it_exists(self, id):
        elements = self._driver.find_elements_by_id(id)
        if elements:
            return elements[0]
        else:
            return False

    def _submit_button(self, field_id):
        return self._driver.find_element_by_id(field_id)

    def navigate_to_login_page(self):
        self._driver.get(LOGIN_URL)
        time.sleep(5)

    def set_email(self, name):
        field = self.it_exists(LoginPageLocators.ELEMENT_IDS["FIELDS"]["EMAIL"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def set_password(self, name):
        field = self.it_exists(LoginPageLocators.ELEMENT_IDS["FIELDS"]["PASSWORD"])
        field.click()
        field.send_keys(name)
        field.send_keys(Keys.RETURN)
        time.sleep(1)

    def credentials_accepted(self):
        button = self._submit_button(LoginPageLocators.ELEMENT_IDS["BUTTON"])
        assert_that(button.is_displayed(), equal_to(True))
        assert_that(button.is_enabled(), equal_to(True))
        button.click()
        print("submitted")
        time.sleep(3)
        assert self._driver.page_source.find("You don't have any docks in here")


class DocksPage(BasePage):

    def it_exists(self, id):
        elements = self._driver.find_elements_by_id(id)
        if elements:
            return elements[0]
        else:
            return False

    def _logout_button(self, field_id):
        return self._driver.find_element_by_id(field_id)

    def logout_deskguru(self):
        button = self._driver.find_element_by_class_name('general-routes').find_element_by_xpath('//div[@title="Logout"]')
        #button = self._driver.find_element_by_class_name('general-routes').find_element_by_xpath(ELEMENT_IDS['XPATH']['LOGOUT_BUTTON'])
        #button = self._logout_button(DockPageLocators.ELEMENT_IDS["XPATH"]["LOGOUT_BUTTON"])
        assert_that(button.is_displayed(), equal_to(True))
        assert_that(button.is_enabled(), equal_to(True))
        button.click()
        print("logging out")
        time.sleep(3)
        assert self._driver.page_source.find("Log into your account")


class TestTemplate(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(BASE_URL)
        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


class TestRegisterAndLoginFlow(TestTemplate):

    def _test_register_user(self):
        register_page = RegisterPage(self.driver)
        register_page.navigate_to_register_page()
        register_page.set_name("Luna Landing")
        register_page.set_company("Pie")
        print(whoami + " registered")
        register_page.set_email(whoami + os.environ['ADDRESS'])
        register_page.set_password("1Password")
        register_page.new_user_is_accepted()

    def _test_login_user(self):
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        print(whoami + " login")
        login_page.set_email(whoami + os.environ['ADDRESS'])
        login_page.set_password("1Password")
        login_page.credentials_accepted()
        time.sleep(2)

    def _test_logout_user(self):
        docks_page = DocksPage(self.driver)
        docks_page.logout_deskguru()
        time.sleep(2)

    def test_registration(self):
        self._test_register_user()
        self._test_login_user()
        self._test_logout_user()


if __name__ == '__main__':
    unittest.main()
