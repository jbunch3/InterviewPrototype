import pdb
import abc
import pandas as pd
from typing import List
from dataclasses import dataclass


class FinancialEntity(metaclass=abc.ABCMeta):
    """Abstract Class / Interface for Financial Entity (Financial Entity)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'process_data') and 
                callable(subclass.process_data))
    
    @abc.abstractmethod
    def process_data(self):
        """Load data into correct format required by entity"""
        raise NotImplementedError

@dataclass
class Table(FinancialEntity):
    imported_table: dict
       
    def process_data(self):        
        self.processed_table = pd.DataFrame(self.imported_table)    

@dataclass
class Text(FinancialEntity):
    imported_header: str
    imported_text: List[str]
    
    def process_data(self):
        self.process_text = self.imported_header
        self.processed_text = self.imported_text