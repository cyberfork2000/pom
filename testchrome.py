import time
import unittest
from selenium import webdriver
from hamcrest import assert_that, equal_to

BASE_URL = 'http://localhost'
LOGIN_URL = BASE_URL + '/signin'


class BasePage(object):

    def __init__(self, driver):
        self._driver = driver


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


class TestLoginPage(TestTemplate):

    def test_login_page(self):
        login_page = LoginPage(self.driver)
        login_page.user_login()
        login_page.check_login()


if __name__ == '__main__':
    unittest.main()
