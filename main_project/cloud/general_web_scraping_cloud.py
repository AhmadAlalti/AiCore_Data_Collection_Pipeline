import time
from pydantic import validate_arguments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class GeneralScraperCloud():

    @validate_arguments
    def __init__(self, URL: str):
        
        
        '''This class is a geenral scraper that can be used to scrape any website
        
        Parameters
        ----------
        URL : str
            A string of the URL of the website you want to scrape
        '''
        
        
        print("------Are you ready to scrape?!------Let's do this!------")
        options = Options()
        options.headless = True        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(URL)



    @validate_arguments
    def close_signup(self, signup_close_button_xpath: str):
        
        
        '''This function waits for the signup button to be clickable, then clicks it
        
        Parameters
        ----------
        signup_close_button_xpath : str
            A string of the xpath of the close button on the signup modal
        '''
        
        
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, signup_close_button_xpath))).click()
        print("Signup pop up has been closed")
    
    
    
    @validate_arguments
    def accept_cookies(self, iframe_id: None, accept_cookies_button_xpath: str):
        
        
        '''It switches to the iframe if provided, waits for the accept cookies button to be clickable, and then clicks it
        
        Parameters
        ----------
        iframe_id : str
            A string of the id of the iframe that contains the cookie consent button
        accept_cookies_button_xpath : str
            A string of he xpath of the button that accepts cookies
        '''
        
        
        try:
            self.driver.switch_to.frame(iframe_id)
            print("Switched to the correct iframe if any")
        except:
            pass
        
        try:
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, accept_cookies_button_xpath))).click()
            print("Accept cookies button has been clicked")
        except:
            pass



    @validate_arguments
    def open_desired_category_link(self, desired_category_xpath: str):
       
        
        '''Finds the category you want to scrape and opens its link
        
        Parameters
        ----------
        desired_category_xpath : str
            The xpath of the category you want to open
        '''
        
        
        category_a_tag = self.driver.find_element(by=By.XPATH, value=desired_category_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", category_a_tag)
        self.category_link = category_a_tag.get_attribute('href')
        self.driver.get(self.category_link)
        print("Desired category link was opened")



    @validate_arguments
    def get_object_links(self, container_xpath: str, objects_list_relative_xpath: str):
        
        
        '''A function that gets the links of the objects you want and stores them in a list
        
        Parameters
        ----------
        container_xpath : str
            A string of the xpath of the container that holds the list of objects
        objects_list_relative_xpath : str
            A string of the xpath of the list of objects that you want to get the links for
        
        Returns
        -------
        list
            A list of links representing each object to be scraped
        '''
        
        
        container = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, container_xpath)))
        object_list = container.find_elements(by=By.XPATH, value=objects_list_relative_xpath) 
        links = []
        
        for product in object_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            links.append(link)
        
        print("The links of the objects on this page have been saved")
        return links
    
    
    @validate_arguments
    def get_all_objects(self, pages: int, container_xpath: str, objects_list_relative_xpath: str, next_button_xpath: str):
       
       
        '''This function moves through pages and gets the links of all the objects to be scraped
        
        Parameters
        ----------
        pages : int
            number of pages to scrape
        container_xpath : str
            the xpath of the container that holds the objects you want to scrape
        objects_list_relative_xpath : str
            the xpath of the list of objects relative to the container_xpath
        next_button_xpath : str
            the xpath of the next button
        
        Returns
        -------
        list
            A list of all the object links on the different pages
        '''
        
        
        all_objects_list = []
        self.pages = pages
        all_objects_list.extend(self.get_object_links(container_xpath, objects_list_relative_xpath))
        
        for page in range(self.pages): 
            next_button = self.driver.find_element(by=By.XPATH, value=next_button_xpath)
            self.driver.execute_script("arguments[0].click();", next_button)
            print("The next page was opened")
            time.sleep(5)
            all_objects_list.extend(self.get_object_links(container_xpath, objects_list_relative_xpath))
            
        return all_objects_list