# Importing the necessary libraries for the class to work.
import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# This class is a general scraper that can be used to scrape any website.
class GeneralScraper():

    def __init__(self, URL, *args, **kwargs):
        '''The function takes in a URL, and then opens a webdriver in Safari, and then goes to the URL
        
        Parameters
        ----------
        URL
            The URL of the website you want to scrape
        
        '''
        super(GeneralScraper, self).__init__(*args, **kwargs)
        self.driver = webdriver.Safari()
        self.driver.get(URL)

    def close_signup(self, signup_close_button_xpath):
        '''This function waits for the signup button to be clickable, then clicks it
        
        Parameters
        ----------
        signup_close_button_xpath
            The xpath of the close button on the signup modal
        
        '''
        signup_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, signup_close_button_xpath)))
        signup_button.click()
    
    def accept_cookies(self, iframe_id, accept_cookies_button_xpath):
        '''It switches to the iframe if provided, waits for the accept cookies button to be clickable, and then clicks it
        
        Parameters
        ----------
        iframe_id
            The id of the iframe that contains the cookie consent button.
        accept_cookies_button_xpath
            The xpath of the button that accepts cookies.
        
        '''
        try:
            self.driver.switch_to.frame(iframe_id)
        except:
            pass
        try:
            accept_cookies_button = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, accept_cookies_button_xpath)))
            accept_cookies_button.click()
        except:
            pass

    def open_desired_category_link(self, desired_category_xpath):
        '''It takes in a desired category xpath, finds the a tag element, scrolls to it, and then gets the href
        attribute of the a tag element
        
        Parameters
        ----------
        desired_category_xpath
            The xpath of the category you want to open.
        
        '''
        category_a_tag = self.driver.find_element(by=By.XPATH, value=desired_category_xpath)
        self.driver.execute_script("arguments[0].scrollIntoView();", category_a_tag)
        self.category_link = category_a_tag.get_attribute('href')
        return self.driver.get(self.category_link)

    def get_object_links(self, container_xpath, objects_list_relative_xpath):
        '''It takes a container xpath and a relative xpath to the objects you want to get the links from, and
        returns a list of links
        
        Parameters
        ----------
        container_xpath
            the xpath of the container that holds the list of objects
        objects_list_relative_xpath
            This is the xpath of the list of objects that you want to get the links for.
        
        Returns
        -------
            A list of links
        
        '''
        container = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, container_xpath)))
        object_list = container.find_elements(by=By.XPATH, value=objects_list_relative_xpath) 
        links = []
        
        for product in object_list:
            a_tag = product.find_element(by=By.TAG_NAME, value='a')
            link = a_tag.get_attribute('href')
            links.append(link)
        return links
    
    def get_all_objects(self, pages, container_xpath, objects_list_relative_xpath, next_button_xpath):
        '''This function takes in the number of pages to scrape, the xpath of the container that holds the
        objects, the xpath of the objects relative to the container, and the xpath of the next button. It
        then returns a list of all the objects on all the pages
        
        Parameters
        ----------
        pages
            number of pages to scrape
        container_xpath
            the xpath of the container that holds the objects you want to scrape
        objects_list_relative_xpath
            the xpath of the list of objects relative to the container_xpath
        next_button_xpath
            the xpath of the next button
        
        Returns
        -------
            A list of all the objects on the page.
        
        '''
        self.all_object_list = []
        self.pages = pages
        for i in range(self.pages): 
            self.all_object_list.extend(self.get_object_links(container_xpath, objects_list_relative_xpath))
            next_button = self.driver.find_element(by=By.XPATH, value=next_button_xpath)
            self.driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)


    def get_properties(self, dict_properties):
        '''The function takes a dictionary of properties as input, and returns a dictionary of properties with
        the values scraped from the website
        
        Parameters
        ----------
        dict_properties
            This is a dictionary of the properties that you want to scrape. The key is the name of the property
        and the value is a tuple of the xpath and the attribute that you want to scrape.
        
        Returns
        -------
            A dictionary with the keys being the property names and the values being a list of the property
        values.
        
        '''
        properties_data = {k: [] for k in dict_properties.keys()}
        for link in self.all_object_list[:2]:
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

    def generate_uuid(self, complete_properties_data):
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
        for link in self.all_object_list[:2]:
            object_uuid = str(uuid.uuid4())
            complete_properties_data['UUID'].append(object_uuid)
        return complete_properties_data