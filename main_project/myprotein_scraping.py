# Importing the modules that are needed for the class to work.
import general_web_scraping
import data_handling
import configuration_file

# This class inherits from the GeneralScraper class and the DataHandling class.
class MyProtein(general_web_scraping.GeneralScraper, data_handling.DataHandling):

    def __init__(self, URL, raw_data_path):
        '''The above function is the constructor of the class MyProtein. It is called when an object of the
        class is created.
        
        Parameters
        ----------
        URL
            The URL of the website you want to scrape.
        raw_data_path
            The path where you want to save the raw data.
        
        '''
        super(MyProtein, self).__init__(URL, raw_data_path)
        self.close_signup(configuration_file.SIGN_UP_CLOSE_BUTTON_XPATH)
        self.accept_cookies(configuration_file.IFRAME_ID, configuration_file.ACCEPT_COOKIES_BUTTON_XPATH)
        self.open_desired_category_link(configuration_file.DESIRED_CATEGORY_XPATH)
        self.get_all_objects(configuration_file.PAGES,configuration_file.CONTAINER_XPATH, configuration_file.OBJECT_LIST_RELATIVE_XPATH, configuration_file.NEXT_BUTTON_XPATH)
        dict_data = self.get_properties(configuration_file.DICT_PROPERTIES)
        complete_dict = self.generate_uuid(dict_data)
        self.create_raw_data_folder()
        self.save_data_locally(complete_dict, configuration_file.BUCKET_NAME)
        self.download_image(complete_dict, configuration_file.BUCKET_NAME)

# A way to run the main function in a Python script.
if __name__ == "__main__":
    MyProtein(configuration_file.URL, configuration_file.RAW_DATA_PATH)