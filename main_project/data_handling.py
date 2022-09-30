from http import client
import boto3
import json
import os
import urllib.request
import tempfile

class DataHandling():
    
    def __init__(self, bucket_name, *args, **kwargss):
        super(DataHandling, self).__init__(*args, **kwargss)
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name
    
    def save_data(self, complete_properties_data):
        temp_file = tempfile.NamedTemporaryFile(mode="w+")
        json.dump(complete_properties_data, temp_file)
        temp_file.flush()
        self.s3_client.upload_file(temp_file.name, self.bucket_name, 'data.json')     

    def download_image(self, complete_properties_data):
        image_name_and_link = zip(complete_properties_data["Unique_ID"], complete_properties_data["Product_Image"])
        self.s3_client.put_object(Bucket=self.bucket_name, Key=('images/'))
        for image_data in image_name_and_link:
            with tempfile.TemporaryDirectory() as tmpdir:
                # with open(image_path + f'{image_data[0]}.jpg', 'w'):
                urllib.request.urlretrieve(image_data[1], tmpdir+ f'{image_data[0]}.jpg')
                self.s3_client.upload_file(tmpdir + f'{image_data[0]}.jpg', self.bucket_name, 'images/{}'.format(f'{image_data[0]}.jpg'))
                
