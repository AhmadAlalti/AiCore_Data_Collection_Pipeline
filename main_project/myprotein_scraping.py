import general_web_scraping
import data_handling
import configuration_file
from pydantic import validate_arguments


class MyProtein(general_web_scraping.GeneralScraper, data_handling.DataHandling):

    @validate_arguments
    def __init__(self, URL: str, bucket_name: str):
        
        
        '''The class inherits 2 classes and runs them together to scrape and handle data
        
        Parameters
        ----------
        URL : str
            The URL of the website you want to scrape.
        bucket_name : str
            A string of the bucket name where you want to save your data
        '''
        
        
        super(MyProtein, self).__init__(URL, bucket_name)
        self.close_signup(configuration_file.SIGN_UP_CLOSE_BUTTON_XPATH)
        self.accept_cookies(configuration_file.IFRAME_ID, configuration_file.ACCEPT_COOKIES_BUTTON_XPATH)
        self.open_desired_category_link(configuration_file.DESIRED_CATEGORY_XPATH)
        self.get_all_objects(configuration_file.PAGES,configuration_file.CONTAINER_XPATH, configuration_file.OBJECT_LIST_RELATIVE_XPATH, configuration_file.NEXT_BUTTON_XPATH)
        dict_data = self.get_properties(configuration_file.DICT_PROPERTIES)
        complete_dict = self.generate_uuid(dict_data)
        self.save_data(complete_dict)
        self.download_image(complete_dict)
        self.data_to_db()



if __name__ == "__main__":
    MyProtein(configuration_file.URL, configuration_file.BUCKET_NAME)