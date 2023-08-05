import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FlaskAppSeleniumTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # Change to the appropriate WebDriver for your browser
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        self.driver.get('http://127.0.0.1:5000/')
        self.assertIn('Welcome to MovieWeb App', self.driver.page_source)

    def test_users_page(self):
        self.driver.get('http://127.0.0.1:5000/users')
        self.assertIn('<h1>Users</h1>', self.driver.page_source)

    def test_add_new_user(self):
        self.driver.get('http://127.0.0.1:5000/add_user')
        input_element = self.driver.find_element_by_id('name')
        input_element.send_keys('Test User')
        input_element.send_keys(Keys.RETURN)
        self.assertIn('Test User', self.driver.page_source)

    def test_add_duplicate_user(self):
        self.driver.get('http://127.0.0.1:5000/add_user')
        input_element = self.driver.find_element_by_id('name')
        input_element.send_keys('Test User')
        input_element.send_keys(Keys.RETURN)
        self.assertIn('User already exist', self.driver.page_source)

    def test_add_new_movie(self):
        self.driver.get('http://127.0.0.1:5000/users/1/add_movie')
        input_element = self.driver.find_element_by_id('title')
        input_element.send_keys('Test Movie')
        input_element.send_keys(Keys.RETURN)
        self.assertIn('Test Movie', self.driver.page_source)

    def test_add_duplicate_movie(self):
        self.driver.get('http://127.0.0.1:5000/users/1/add_movie')
        input_element = self.driver.find_element_by_id('title')
        input_element.send_keys('Test Movie')
        input_element.send_keys(Keys.RETURN)
        self.assertIn('Movie already exist', self.driver.page_source)


if __name__ == '__main__':
    unittest.main()
