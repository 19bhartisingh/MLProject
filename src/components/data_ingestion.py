import os 
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from components.data_transformation import DataTransformation
from components.data_transformation import DataTransformationConfig
from components.model_trainer import ModelTrainer
from components.model_trainer import ModelTrainerConfig

current_dir = os.path.dirname(os.path.abspath('src\components\data_ingestion.py'))  # Get the current file's directory
root_dir = os.path.abspath(os.path.join(current_dir, "src"))  # Navigate two levels up to the project root
sys.path.append(root_dir)  

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"raw.csv")
    

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):
        # reading the data
        logging.info("Entered the data ingestion method or component")
        try :
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info("Read the dataset as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test splitinitiated.")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Ingestion of the data is completed.")
            
            return (
                
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
        

if __name__=="__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()
    
    data_transformation = DataTransformation()
    train_arr,test_arr = data_transformation. initiate_data_transformation(train_data,test_data)
    
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))
    