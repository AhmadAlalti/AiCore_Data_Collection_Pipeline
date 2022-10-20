import boto3
import json
import pandas as pd
import tempfile
import time
import urllib.request
import uuid
from main_project.general_web_scraping import GeneralScraper
from pydantic import validate_arguments
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine



class DataHandling(GeneralScraper):
    
    @validate_arguments
    def __init__(self, URL: str, bucket_name: str, *args, **kwargss):
        
        
        '''This class handles the data that will be scraped from the website of choice
        
        Parameters
        ----------
        URL : str
            The URL of the website you want to scrape
        bucket_name : str
            The name of the bucket you want to upload to.
        '''


        super(DataHandling, self).__init__(URL, *args, **kwargss)
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'aicoredatacollectiondb.cqldyrxhfamt.eu-west-2.rds.amazonaws.com' 
        USER =  'postgres'
        PASSWORD = 'postgres'
        PORT = 5432
        DATABASE = 'postgres'
        self.engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", pool_pre_ping=True)
        


    @validate_arguments
    def get_properties(self, dict_properties: dict):
        
        
        '''The function takes a dictionary of properties as input, and returns a dictionary of properties with
        values
        
        Parameters
        ----------
        dict_properties : dict
            This is a dictionary of properties that you want to extract from the page. The key is the name of
        the property and the value is a tuple of the xpath and the attribute to extract.
        
        Returns
        -------
            A dictionary with the keys being the property names and the values being the property values.
        '''
        
        properties_data = {k: str for k in dict_properties.keys()}
        
        for key, value in dict_properties.items():
            try:
                if value[1] == 'text':
                    property_value = self.driver.find_element(by=By.XPATH, value=value[0]).text
                    properties_data[key] = property_value.strip()
                else:
                    property_value = self.driver.find_element(by=By.XPATH, value=value[0]).get_attribute(value[1])
                    properties_data[key] = property_value.strip()
            except:
                    properties_data[key] = "Not Applicable"   
        
        return properties_data
    
    
    
    @validate_arguments
    def generate_uuid(self, properties_data_uuid: dict):
        
        
        '''This function generates a UUID for each object in the dictionary
        
        Parameters
        ----------
        properties_data_uuid : dict
            a dictionary containing the properties of the object
        
        Returns
        -------
            A dictionary with a list of UUIDs
        '''
        
        
        properties_data_uuid['UUID'] = []
        object_uuid = str(uuid.uuid4())
        properties_data_uuid['UUID'].append(object_uuid)
                    
        return properties_data_uuid



    @validate_arguments
    def save_image(self, complete_dict: dict):
       
       
        '''It takes a dictionary as an argument, downloads the image from the URL in the dictionary, and
        uploads it to the S3 bucket
        
        Parameters
        ----------
        complete_dict : dict
            This is the dictionary that contains all the information about the product.
        '''
        
        
        with tempfile.TemporaryDirectory() as tmpdir:
            urllib.request.urlretrieve(complete_dict["Product_Image"], tmpdir+ f'{complete_dict["Unique_ID"]}.jpg')
            self.s3_client.upload_file(tmpdir + f'{complete_dict["Unique_ID"]}.jpg', self.bucket_name, 'images/{}'.format(f'{complete_dict["Unique_ID"]}.jpg'))



    @validate_arguments
    def save_properties(self, dict_properties: dict):
        
        
        '''This function takes in a dictionary of properties, generates a UUID for each property, and then
        uploads the data to an S3 bucket.
        
        Parameters
        ----------
        dict_properties : dict
            This is the dictionary of properties that you want to save.
        '''
        
        
        dict_of_data = self.get_properties(dict_properties)
        self.complete_dict = self.generate_uuid(dict_of_data)
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(self.complete_dict, self.temp_file, indent=4)
        self.temp_file.flush()
        self.s3_client.upload_file(self.temp_file.name, self.bucket_name, 'json_data/{}'.format(f'{self.complete_dict["Unique_ID"]}_data.json'))                   
    


    @validate_arguments
    def create_df(self, dict_properties: dict):
        
        
        '''It creates a dataframe with the columns of the dictionary keys and a column for the UUID
        
        Parameters
        ----------
        dict_properties : dict
            a dictionary of the properties of the object you want to create.
        '''
        
        
        list_of_dict_keys = [*dict_properties]
        self.list_of_columns = list_of_dict_keys + ["UUID"]
        self.df_initial = pd.DataFrame(columns=self.list_of_columns)
        self.engine.connect()
        self.df_initial.to_sql('objects_data', con=self.engine, if_exists='append', index=False)
    
    
    
    def get_unique_id(self):
        
        
        '''This function is used to get the unique id's of the objects that are already present in the
        database.
        '''
        
        
        self.df_with_id = pd.read_sql_query("SELECT * FROM objects_data", self.engine)
        self.unique_id_list = self.df_with_id['Unique_ID'].values.tolist()



    @validate_arguments
    def get_and_upload_all_data(self, all_objects_list: list, dict_properties: dict):
        
        
        '''This function takes in a list of all the links to the objects and a dictionary of the properties
        that we want to extract from the website. It then iterates through the list of links and extracts
        the properties from each link and saves it in a dictionary. It then checks if the unique ID of the
        object is already in the database. If it is, it skips the object. If it isn't, it uploads the
        dictionary to the database and saves the image of the object.
        
        Parameters
        ----------
        all_objects_list : list
            list of all the links to the objects
        dict_properties : dict
            This is a dictionary of all the properties that you want to scrape.
        '''
           
                
        for link in all_objects_list[:4]:
            self.driver.get(link)
            time.sleep(2)
            self.save_properties(dict_properties)
            
            if self.complete_dict["Unique_ID"] in self.unique_id_list:
                pass
            else:
                df_dictionary = pd.DataFrame(self.complete_dict)
                print(df_dictionary)
                self.engine.connect()
                df_dictionary.to_sql('objects_data', con=self.engine, if_exists='append', index=False)
                self.save_image(self.complete_dict)
                self.unique_id_list.append(self.complete_dict["Unique_ID"])