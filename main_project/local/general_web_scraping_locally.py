import time
import uuid
from pydantic import validate_arguments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class GeneralScraperLocal():

    @validate_arguments
    def __init__(self, URL: str, *args, **kwargs):
        
        
        '''This class is a geenral scraper that can be used to scrape any website
        
        Parameters
        ----------
        URL : str
            A string of the URL of the website you want to scrape
        '''
        
        super(GeneralScraperLocal, self).__init__(*args, **kwargs)
        print("------Are you ready to scrape?!------Let's do this!------")
        options = Options()
        options.headless = True    
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")        
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
        
        
        self.all_objects_list = []
        self.pages = pages
        self.all_objects_list.extend(self.get_object_links(container_xpath, objects_list_relative_xpath))
        
        for page in range(self.pages): 
            next_button = self.driver.find_element(by=By.XPATH, value=next_button_xpath)
            self.driver.execute_script("arguments[0].click();", next_button)
            print("The next page was opened")
            time.sleep(5)
            self.all_objects_list.extend(self.get_object_links(container_xpath, objects_list_relative_xpath))
    


    @validate_arguments
    def get_properties(self, dict_properties: dict):
       
       
        '''The function returns a dictionary of properties with the values scraped from the website

        Parameters
        ----------
        dict_properties : dict
            This is a dictionary of the properties that you want to scrape. The key is the name of the property
        and the value is a tuple of the xpath and the attribute that you want to scrape.
        
        Returns
        -------
            A dictionary with the keys being the property names and the values being a list of the property
        values.
        '''
        
        
        properties_data = {k: [] for k in dict_properties.keys()}

        for link in self.all_objects_list[:5]:
            self.driver.get(link)
            time.sleep(2)
            
            for key, value in dict_properties.items(): 
                try:
                    if value[1] == 'text':
                        property_value = self.driver.find_element(by=By.XPATH, value=value[0]).text
                        properties_data[key].append(property_value.strip())
                    else:
                        property_value = self.driver.find_element(by=By.XPATH, value=value[0]).get_attribute(value[1])
                        properties_data[key].append(property_value.strip())
                except:
                        properties_data[key].append("Not Applicable")     
                        
        return properties_data



    @validate_arguments
    def generate_uuid(self, complete_properties_data: dict):
        
        
        '''This function generates a UUID for each object in the list of objects
        
        Parameters
        ----------
        complete_properties_data
            This is a dictionary that contains all the properties of the object.
        
        Returns
        -------
            The complete_properties_data dictionary is being returned with the UUIDs now added.
        '''
        
        
        complete_properties_data['UUID'] = []
        
        for link in self.all_objects_list[:5]:
            
            object_uuid = str(uuid.uuid4())
            complete_properties_data['UUID'].append(object_uuid)
            
        return complete_properties_data