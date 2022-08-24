import unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests


class ChromeSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def test_search_in_python_org(self):
        """ Test if a given text is correctly returned """

        print("Performing test1")

        driver = self.driver
        driver.get("https://www.python.org")  # go to this page
        self.assertIn("Python", driver.title)  # assert website title
        elem = driver.find_element(By.NAME, "q")  # find query field
        elem.send_keys("getting started with python")  # with this text
        elem.send_keys(Keys.RETURN)  # send Enter

        assert "https://www.python.org/search/?q=getting+started+with+python&submit=" == driver.current_url  # assert the current url

    def test_is_jobs_url_valid(self):
        """ Test if Community page has loaded and is valid"""

        print("Performing test2")

        driver = self.driver
        driver.get("https://www.python.org")
        elem = driver.find_element("xpath", "//a[contains(@href,'community-landing')]")  # find elem by 'a href' text

        # wait 5 seconds, ensure elem2 is already present
        delay = 5
        try:
            elem_is_present = EC.presence_of_element_located((By.CLASS_NAME, 'menu'))
            WebDriverWait(driver, delay).until(elem_is_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        elem.click()  # click on element
        elem2 = driver.find_element("xpath", "//a[contains(@href,'community/jobs')]")  # find elem by 'a href' text
        elem2.click()

        elem3 = driver.find_element(By.CSS_SELECTOR, 'a.reference.external').get_attribute('href')
        request_response = requests.head(elem3)
        status_code = request_response.status_code

        self.assertEqual(200, status_code)
        self.assertEqual('https://www.python.org/jobs/', elem3)

    def tearDown(self):
        """ Close Chrome window """
        self.driver.close()  # close the browser window

if __name__ == "__main__":
    unittest.main()
