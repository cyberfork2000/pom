import time
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

    print("BASE PAGE CLASS")

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

    print("REGISTER PAGE CLASS")

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
        assert self._driver.page_source.find("Activate your account")
        # WebDriverWait(self._driver, 15).until(EC.url_changes(expected_url))
        # assert_that(self._driver.find_elements_by_id(RegisterPageLocators.ELEMENT_IDS["RESEND"]), equal_to(True))
        # button = self._submit_button(RegisterPageLocators.ELEMENT_IDS["RESEND"])
        # assert_that(button.is_displayed(), equal_to(True))
        # assert_that(button.is_enabled(), equal_to(True))


class LoginPage(BasePage):

    print("LOGIN PAGE CLASS")

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

    # def enter_credentials(self, username, password):
    #     print("EMTER CREDENTIALS")
    #     field = self.it_exists(LoginPageLocators.ELEMENT_IDS["FIELDS"]["EMAIL"])
    #     field = self.find_element_by_id(LoginPageLocators.ELEMENT_IDS["FIELDS"]["EMAIL"])
    #     field.click()
    #     field.send_keys(username)
    #     #field.send_keys(Keys.RETURN)
    #     field = self.it_exists(LoginPageLocators.ELEMENT_IDS["FIELDS"]["PASSWORD"])
    #     field = self.find_element_by_id(LoginPageLocators.ELEMENT_IDS["FIELDS"]["PASSWORD"])
    #     field.click()
    #     field.send_keys(password)
    #     # field.send_keys(Keys.RETURN)
    #     # button = self.it_exists((self, LoginPageLocators.ELEMENT_IDS["BUTTON"]))
    #     # time.sleep(2)

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
        print("ACCEPT CREDENTIALS")
        #button = self.it_exists((self, LoginPageLocators.ELEMENT_IDS["BUTTON"]))
        button = self._submit_button(LoginPageLocators.ELEMENT_IDS["BUTTON"])
        assert_that(button.is_displayed(), equal_to(True))
        assert_that(button.is_enabled(), equal_to(True))
        print(self._driver.title)
        button.click()
        print("submitted")
        time.sleep(3)
        assert self._driver.page_source.find("You don't have any docks in here")


class TestTemplate(unittest.TestCase):

    print("TEST TEMPLATE CLASS")

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
        register_page.set_email(whoami + "@example.com")
        register_page.set_password("1Password")
        register_page.new_user_is_accepted()

    def _test_login_user(self):
        login_page = LoginPage(self.driver)
        login_page.navigate_to_login_page()
        print(whoami + " login")
        #login_page.enter_credentials(whoami + "@example.com", "1Password")
        login_page.set_email(whoami + "@example.com")
        login_page.set_password("1Password")
        login_page.credentials_accepted()
        time.sleep(5)
        #login_page.credentials_accepted()

    def test_registration(self):
        self._test_register_user()
        self._test_login_user()



if __name__ == '__main__':
    unittest.main()
