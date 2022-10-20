import sys
sys.path.append("../..")
from main_project import configuration_file
from main_project.cloud.data_handling_cloud import DataHandlingCloud
from pydantic import validate_arguments


class MyProtein(DataHandlingCloud):

    @validate_arguments
    def __init__(self, URL: str, bucket_name: str):
        
        
        '''The class runs to scrape and handle data at the same time
        
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
        list_of_links = self.get_all_objects(configuration_file.PAGES,configuration_file.CONTAINER_XPATH, configuration_file.OBJECT_LIST_RELATIVE_XPATH, configuration_file.NEXT_BUTTON_XPATH)
        self.create_df(configuration_file.DICT_PROPERTIES)
        self.get_unique_id()
        self.get_and_upload_all_data(list_of_links, configuration_file.DICT_PROPERTIES)



if __name__ == "__main__":
    MyProtein(configuration_file.URL, configuration_file.BUCKET_NAME)