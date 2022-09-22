# These are the libraries that are being imported to be used in the class.
import json
import os
import urllib.request

# This class is used to handle data.
class DataHandling():
    
    def __init__(self, raw_data_path, *args, **kwargss):
        '''> The `__init__` function is a special function that is called when an object is created from a
        class and it allows the class to initialize the attributes of the class
        
        Parameters
        ----------
        raw_data_path
            The path to the raw data.
        
        '''
        super(DataHandling, self).__init__(*args, **kwargss)
        self.raw_data_path = raw_data_path

    def create_raw_data_folder(self):
        '''It creates a folder called 'raw_data' if it doesn't already exist in your parent directory
        
        '''
        try:
            raw_data_directory = os.mkdir(self.raw_data_path)
        except FileExistsError:
            print("File already exists")
        return raw_data_directory
    
    def save_data_locally(self, complete_properties_data):
        '''It takes the data from the API and saves it locally as a JSON file.
        
        Parameters
        ----------
        complete_properties_data
            This is the data that we want to save.
        
        '''
        with open(self.raw_data_path + '/data.json', 'w') as all_data:
            json.dump(complete_properties_data, all_data)     

    def download_image(self, complete_properties_data):
        '''It takes the dataframe with all the properties data, and downloads the images from the links in the
        dataframe, and saves them in a folder called 'images' in the 'raw_data' folder with the Unique_ID as their names
        
        Parameters
        ----------
        complete_properties_data
            This is the dataframe that contains all the data that we need to download the images.
        
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
