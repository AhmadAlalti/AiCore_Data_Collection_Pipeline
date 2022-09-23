import json
import os
import shutil
import sys
sys.path.append("..")
import unittest
from main_project.data_handling import DataHandling

class TestDataHandling(unittest.TestCase):
    
    def setUp(self):
        self.test_path = "../test_raw_data_path"
        self.data_handler = DataHandling(self.test_path)
        self.test_complete_dictionary = { 
            "Name" : "",
            "Unique_ID" : ["10530943", "12081395"], 
            "UUID" :"", 
            "Product_Image" : ["https://static.thcdn.com/images/large/original//productimg/1600/1600/10530943-1224889444460882.jpg", "https://static.thcdn.com/images/large/original//productimg/1600/1600/12081397-1324792209160155.jpg"]
            }
            
    def test1_create_raw_data_folder(self):
        self.data_handler.create_raw_data_folder() 
        self.assertTrue(os.path.exists(self.test_path))
        print("Raw data file path exists")   
        
    def test2_save_data_locally(self):
        self.data_handler.save_data_locally(self.test_complete_dictionary)
        self.assertTrue(os.path.exists(self.test_path + '/data.json'))
        with open(self.test_path + '/data.json', 'r') as all_data:
            complete_data = json.load(all_data) 
        json_keys = complete_data.keys()
        your_dictionary_keys = list(self.test_complete_dictionary.keys())
        self.assertEqual(set(json_keys), set(your_dictionary_keys))
        print("Json exists and has the correct keys")

    def test3_download_image(self):
        self.data_handler.download_image(self.test_complete_dictionary)
        self.assertTrue(os.path.exists(self.test_path + '/images'))
        print("Images file path exists")
        
    def test4_download_image(self):
        self.data_handler.download_image(self.test_complete_dictionary)
        image_files_list = os.listdir(self.test_path + '/images')
        for file_name in image_files_list :
            name, extension = os.path.splitext(file_name)
            self.assertEqual(extension, ".jpg")
            file_name_index = image_files_list.index(file_name)
            self.assertEqual(name, self.test_complete_dictionary["Unique_ID"][file_name_index])
        print("Images have been stored as .jpg files with the correct names")     
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("../test_raw_data_path")
        pass
        
if __name__ == "__main__":
    unittest.main()