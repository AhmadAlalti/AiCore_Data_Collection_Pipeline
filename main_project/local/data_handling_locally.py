import json
import os
import urllib.request
from pydantic import validate_arguments


class DataHandlingLocal():
    
    @validate_arguments
    def __init__(self, raw_data_path: str, *args, **kwargs):
        
        
        '''This class is used to handle your scraper's data locally
        
        Parameters
        ----------
        raw_data_path : str
            A string representing the path to the raw data
        '''
        
        
        super(DataHandlingLocal, self).__init__(*args, **kwargs)
        self.raw_data_path = raw_data_path



    def create_raw_data_folder(self):
        
        
        '''It creates the raw_data folder in the specified path
        '''
        
        
        try:
            os.mkdir(self.raw_data_path)
        except FileExistsError:
            pass
    
    
    
    @validate_arguments
    def save_data_locally(self, complete_properties_data: dict):
        
        
        '''It takes the data from the API and saves it locally as a JSON file
        
        Parameters
        ----------
        complete_properties_data : dict
            A dictionary of the data scraped that we want to save as a JSON file
        '''
        
        
        with open(self.raw_data_path + '/data.json', 'w') as all_data:
            json.dump(complete_properties_data, all_data, indent=4)   



    @validate_arguments
    def download_image(self, complete_properties_data: dict):


        '''Downloads images and saves them locally
        
        Parameters
        ----------
        complete_properties_data : dict
            A dictionary of the data scraped used to get the links and name the images
        '''
        
        
        try:
            os.mkdir(self.raw_data_path + '/images')
        except FileExistsError:
            pass
        
        image_path = self.raw_data_path + '/images/'
        image_name_and_link = zip(complete_properties_data["Unique_ID"], complete_properties_data["Product_Image"])

        for image_data in image_name_and_link:
                with open(image_path + f'{image_data[0]}.jpg', 'w'):
                    urllib.request.urlretrieve(image_data[1], image_path + f'{image_data[0]}.jpg')
