import sys
sys.path.append("../..")
from main_project import configuration_file
from main_project.local.data_handling_locally import DataHandlingLocal
from main_project.local.general_web_scraping_locally import GeneralScraperLocal
from pydantic import validate_arguments


class MyProtein(GeneralScraperLocal, DataHandlingLocal):

    @validate_arguments
    def __init__(self, URL: str, raw_data_path: str):
        
        
        '''The class runs to scrape and handle data at the same time
        
        Parameters
        ----------
        URL : str
            The URL of the website you want to scrape.
        raw_data_path : str
            A string of the raw data file path you want to save your data in
        '''
        
        
        super(MyProtein, self).__init__(URL, raw_data_path)
        self.close_signup(configuration_file.SIGN_UP_CLOSE_BUTTON_XPATH)
        self.accept_cookies(configuration_file.IFRAME_ID, configuration_file.ACCEPT_COOKIES_BUTTON_XPATH)
        self.open_desired_category_link(configuration_file.DESIRED_CATEGORY_XPATH)
        self.get_all_objects(configuration_file.PAGES,configuration_file.CONTAINER_XPATH, configuration_file.OBJECT_LIST_RELATIVE_XPATH, configuration_file.NEXT_BUTTON_XPATH)
        dict_data = self.get_properties(configuration_file.DICT_PROPERTIES)
        complete_dict = self.generate_uuid(dict_data)
        self.create_raw_data_folder()
        self.save_data_locally(complete_dict)
        self.download_image(complete_dict)



if __name__ == "__main__":
    MyProtein(configuration_file.URL, configuration_file.RAW_DATA_PATH)