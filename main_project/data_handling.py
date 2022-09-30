# These are the libraries that are being imported to be used in the class.
from http import client
import boto3
import json
import os
import urllib.request
import tempfile

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
        self.s3_client = boto3.client('s3')
        self.raw_data_path = raw_data_path

    def create_raw_data_folder(self):
        '''It creates a folder called 'raw_data' if it doesn't already exist in your parent directory
        
        '''
        try:
            os.mkdir(self.raw_data_path)
        except FileExistsError:
            print("File already exists")
    
    def save_data_locally(self, complete_properties_data, bucket_name):
        '''It takes the data from the API and saves it locally as a JSON file.
        
        Parameters
        ----------
        complete_properties_data
            This is the data that we want to save.
        
        '''
        temp_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(complete_properties_data, temp_file)
        self.s3_client.upload_file(temp_file.name, bucket_name, 'data.json')     
        
        # with tempfile.TemporaryFile() as all_data:
        #     read_file = all_data.read()
        #     print(complete_properties_data)
        #     json.dump(complete_properties_data, read_file)
            # self.s3_client.upload_file(all_data, bucket_name, 'data.json')     

    def download_image(self, complete_properties_data, bucket_name):
        '''It takes the dataframe with all the properties data, and downloads the images from the links in the
        dataframe, and saves them in a folder called 'images' in the 'raw_data' folder with the Unique_ID as their names
        
        Parameters
        ----------
        complete_properties_data
            This is the dataframe that contains all the data that we need to download the images.
        
        '''
        # try:
        #     os.mkdir(self.raw_data_path + '/images')
        # except FileExistsError:
        #     pass
        # image_path = self.raw_data_path + '/images/'
        image_name_and_link = zip(complete_properties_data["Unique_ID"], complete_properties_data["Product_Image"])
        self.s3_client.put_object(Bucket=bucket_name, Key=('images/'))
        for image_data in image_name_and_link:
            with tempfile.TemporaryDirectory() as tmpdir:
                # with open(image_path + f'{image_data[0]}.jpg', 'w'):
                urllib.request.urlretrieve(image_data[1], tmpdir+ f'{image_data[0]}.jpg')
                self.s3_client.upload_file(tmpdir + f'{image_data[0]}.jpg', bucket_name, 'images/{}'.format(f'{image_data[0]}.jpg'))
                
