import boto3
import json
import pandas as pd
import tempfile
import time
import urllib.request
import uuid
from general_web_scraping import GeneralScraper
from pydantic import validate_arguments
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine


class DataHandling(GeneralScraper):
    
    def __init__(self, URL: str, bucket_name: str, *args, **kwargss):

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
        
        properties_data_uuid['UUID'] = []
        object_uuid = str(uuid.uuid4())
        properties_data_uuid['UUID'].append(object_uuid)
                    
        return properties_data_uuid

    def save_image(self, complete_dict: dict):
        
        with tempfile.TemporaryDirectory() as tmpdir:
            urllib.request.urlretrieve(complete_dict["Product_Image"], tmpdir+ f'{complete_dict["Unique_ID"]}.jpg')
            self.s3_client.upload_file(tmpdir + f'{complete_dict["Unique_ID"]}.jpg', self.bucket_name, 'images/{}'.format(f'{complete_dict["Unique_ID"]}.jpg'))



    def save_properties(self, dict_properties: dict):
        
        dict_of_data = self.get_properties(dict_properties)
        self.complete_dict = self.generate_uuid(dict_of_data)
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(self.complete_dict, self.temp_file, indent=4)
        self.temp_file.flush()
        self.s3_client.upload_file(self.temp_file.name, self.bucket_name, 'json_data/{}'.format(f'{self.complete_dict["Unique_ID"]}_data.json'))                   
    

    def create_df(self, dict_properties: dict):
        list_of_dict_keys = [*dict_properties]
        self.list_of_columns = list_of_dict_keys + ["UUID"]
        self.df_initial = pd.DataFrame(columns=self.list_of_columns)
        self.engine.connect()
        self.df_initial.to_sql('objects_data', con=self.engine, if_exists='append', index=False)
    
    def get_unique_id(self):
        self.df_with_id = pd.read_sql_query("SELECT * FROM objects_data", self.engine)
        self.unique_id_list = self.df_with_id['Unique_ID'].values.tolist()
        print(self.unique_id_list)

    def get_and_upload_all_data(self, all_objects_list: list, dict_properties: dict):
                
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