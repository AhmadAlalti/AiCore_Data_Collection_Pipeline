import sys
import time
sys.path.append("..")
import unittest
from main_project.general_web_scraping import GeneralScraper
from selenium.webdriver.common.by import By

class TestGeneralScraper(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        URL = "https://www.myprotein.com"
        cls.scraper = GeneralScraper(URL)        
    
    def test1_close_signup(self):
        self.scraper.close_signup("//button[@class='emailReengagement_close_button']")
        email_popup= self.scraper.driver.find_element(by=By.XPATH, value="//div[@data-component='emailReengagement']")
        element_attribute = email_popup.get_attribute("class")
        self.assertEqual(element_attribute, "emailReengagement show hidden")
        print("The email signup close button has been clicked")
    
    def test2_accept_cookies(self):
        self.scraper.accept_cookies(None, "//button[@class='cookie_modal_button']")
        cookies_popup= self.scraper.driver.find_element(by=By.XPATH, value="//div[@class='cookie_modal']")
        element_attribute = cookies_popup.get_attribute("style")
        self.assertEqual(element_attribute, "display: none;")
        print("The accept cookies button has been clicked")        
    
    @classmethod
    def tearDownClass(cls):
        cls.scraper.driver.quit()

if __name__ == "__main__":
    unittest.main()