import boto3
import json
import urllib.request
import tempfile
import pandas as pd
from sqlalchemy import create_engine

class DataHandling():
    
    def __init__(self, bucket_name: str, *args, **kwargss):
        
        
        '''This class handles the data with connection to the cloud (AWS RDS and S3)
        
        Parameters
        ----------
        bucket_name : str
            The name of the bucket you want to upload to
        '''
        
        
        super(DataHandling, self).__init__(*args, **kwargss)
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
    
    
    
    def save_data(self, complete_properties_data: dict):
        
        
        '''It takes a dictionary of data, dumps it into a temporary file, and then uploads that file to S3
        
        Parameters
        ----------
        complete_properties_data : dict
            This is the data that we want to save to S3
        '''
        
        
        self.temp_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(complete_properties_data, self.temp_file, indent=4)
        self.temp_file.flush()
        self.s3_client.upload_file(self.temp_file.name, self.bucket_name, 'data.json')     



    def download_image(self, complete_properties_data: dict):
        
        
        '''Downloads the images from the link in the dictionary and uploads it to
        the S3 bucket
        
        Parameters
        ----------
        complete_properties_data : dict
            A dictionary of the data scraped used to get the links and name the images
        '''
        
        
        image_name_and_link = zip(complete_properties_data["Unique_ID"], complete_properties_data["Product_Image"])
        self.s3_client.put_object(Bucket=self.bucket_name, Key=('images/'))
        for image_data in image_name_and_link:
            with tempfile.TemporaryDirectory() as tmpdir:
                # with open(image_path + f'{image_data[0]}.jpg', 'w'):
                urllib.request.urlretrieve(image_data[1], tmpdir+ f'{image_data[0]}.jpg')
                self.s3_client.upload_file(tmpdir + f'{image_data[0]}.jpg', self.bucket_name, 'images/{}'.format(f'{image_data[0]}.jpg'))
    
    
    
    def data_to_db(self):
        
        
        '''It reads the JSON file into a pandas dataframe, then writes the dataframe to a postgreSQL database
        '''
        
        
        df = pd.read_json(self.temp_file.name)
        self.engine.connect()
        df.to_sql('objects_data', con=self.engine, if_exists='replace')
