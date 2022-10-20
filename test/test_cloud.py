import sys
sys.path.append("..")
import unittest
from main_project.cloud.data_handling_cloud import DataHandlingCloud
from selenium.webdriver.common.by import By



class TestGeneralScraper(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        URL = "https://www.myprotein.com"
        bucket_name = 'aicoredatacollectionbucket'
        cls.scraper = DataHandlingCloud(URL, bucket_name)
        cls.test_dict_properties = {
            'Name': ('//h1[@class="productName_title"]', 'text'), 
            'Starting_Price': ('//p[@data-product-price="price"]', 'text'), 
            'Flavour_Selected': ('//select[@id="athena-product-variation-dropdown-5"]//option[@selected]', 'text'), 
            'Stars': ('//span[@class="athenaProductReviews_aggregateRatingValue"]', 'text'), 
            'Product_Image':('//img[@class="athenaProductImageCarousel_image"]', 'src'), 
            'Unique_ID':('//input[@name="prodId"]', 'value') 
            }
    
    
    
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
    
    
    
    def test3_open_desired_category_link(self):
        
        self.scraper.open_desired_category_link('//*[@id="mainContent"]/div[2]/a[1]')
        current_url = self.scraper.driver.current_url
        self.assertEqual(current_url, 'https://www.myprotein.com/nutrition/protein.list')
        print("The correct category link has been opened")
    
    
    
    def test4_get_object_links(self):
        
        self.__class__.links = self.scraper.get_object_links('//*[@id="mainContent"]/div[3]/ul', './li[contains(@class, "productListProducts_product")]')
        self.assertIsInstance(self.__class__.links, list)
        print("A list of links on the page was returned successfully")
    
    
    
    def test5_get_all_objects(self):
        
        all_objects_list = self.scraper.get_all_objects(2, '//*[@id="mainContent"]/div[3]/ul', './li[contains(@class, "productListProducts_product")]', '//button[contains(@class, "NavigationButtonNext")]')
        self.assertTrue(len(self.__class__.links) < len(all_objects_list))
        print("A list of all the objects on the desired pages was returned correctly")
    
    
    
    def test6_get_properties(self):
       
        self.__class__.test_properties_data = self.scraper.get_properties(self.test_dict_properties)
        self.assertIsInstance(self.__class__.test_properties_data, dict)
        test_properties_data_keys = self.__class__.test_properties_data.keys()
        your_dictionary_keys = list(self.test_dict_properties.keys())
        self.assertEqual(set(test_properties_data_keys), set(your_dictionary_keys))
        print("A dictionary of the properties has been created with the right keys")
    
    
    
    def test7_generate_uuid(self):
   
        complete_dict = self.scraper.generate_uuid(self.__class__.test_properties_data)
        self.assertIn("UUID", complete_dict)
        print("A new complete dict has been created with a new UUID key")
    
    
    
    @classmethod
    def tearDownClass(cls):
        
        cls.scraper.driver.quit()



if __name__ == "__main__":
    unittest.main()