import pdb
import abc
import pandas as pd
from typing import List
from dataclasses import dataclass
from pcapp import data_gateway
from pcapp import report_generator
import re

# this ought to be done with proper database normalization and more robust checks, but for quick implemenation Im doing it here
ASSET_MAPPING = {
        "wind": "Wind Turbine Park",
        "wind park": "Wind Turbine Park",
        "wind turbine park": "Wind Turbine Park",
        "wind thingy": "Wind Turbine Park",
        "solar park": "Solar Park",
        "sun energy": "Solar Park",
        "double flipped twistable reverse note": "Arcane Structured Product",
        "fi derivatives": "Arcane Structured Product",
        "arcane structured product": "Arcane Structured Product",
}

class FinancialEntity(metaclass=abc.ABCMeta):
    """Abstract Class / Interface for Financial Entity (Financial Entity)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'process_data') and 
                callable(subclass.process_data))
        
    @abc.abstractmethod
    def request_data(self):
        """Load data into correct format required by entity"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def process_data(self):
        """Load data into correct format required by entity"""
        raise NotImplementedError
    
@dataclass
class Table(FinancialEntity):
    request: report_generator.ReportRequest

    def request_data(self):
        # Simple logic to determin data source, for large application would be extracted elsewhere
        if self.request.client == 1:
            self.datasource = "data/prod.db"
        else:
            self.datasource = "data/prod.db"
        
        if self.request.debug == True:
            self.datasource = "test_data/test.db"
        
        dataReader = data_gateway.SqlLiteConnection(self.datasource)
        dataReader.load_data_source()
        self.process_request()
        self.imported_table = dataReader.read_table(self.processed_request)
       
    def process_data(self):        
        self.processed_table = pd.DataFrame(self.imported_table)   
        
    def process_request(self):
        # TODO: Needs Error Handling for sure
        match self.request.type:
            case "performance":
                table = "monthly_performance"
            case _:
                table = "monthly_performance"
        
        date = re.match("[0-9]{4}-[0-1]{1}[1-9]{1}-[0-9]{2}", self.request.start_date)
        
        asset = ASSET_MAPPING[self.request.restrictions.lower()]
        
        self.processed_request = {"table": table, "startDate": date.string, "asset": asset}
         

@dataclass
class Text(FinancialEntity):
    request: report_generator.ReportRequest
    
    def request_data(self):
        # Simple logic to determin data source, for large application would be extracted elsewhere
        if self.request.client == 1:
            self.datasource = "data/text_file.txt"
        else:
            self.datasource = "data/text_file.txt"
        
        if self.request.debug == True:
            self.datasource = "test_data/test_file.txt"
        
        # I imagine a more real life scenario is pullint this document from a mongo db or web scraping source
        self.imported_text = data_gateway.TextFileParser(self.datasource)
        self.imported_text.load_data_source()
    
    def process_data(self):
        self.processed_header = self.imported_text.parse_header()
        self.processed_body = self.imported_text.parse_body()