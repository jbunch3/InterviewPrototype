import sqlite3
import pdb
import abc
from typing import List

class DataGateway(metaclass=abc.ABCMeta):
    """Abstract Class / Interface for the Data Repository Design Pattersn (Financial Data Gateway)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'open_data_source') and 
                callable(subclass.open_data_source))
    
    @abc.abstractmethod
    def load_data_source(self):
        """Load data set"""
        raise NotImplementedError

class Connection(DataGateway):
    """Abstract Class for the Connection Class Gateway Objects (Financial Database + Financial Data Mapper)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'read_table') and 
                callable(subclass.read_table))
        
    @abc.abstractmethod
    def read_table(self, path: str, file_name: str) -> dict:
        pass

class Parser(DataGateway):
    """Abstract Class for the Parser Class Gateway Objects (Financial Database + Financial Data Mapper)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'parse_header') and 
                callable(subclass.parse_header) and 
                hasattr(subclass, 'parse_body') and 
                callable(subclass.parse_body))

    @abc.abstractmethod
    def parse_header(self) -> str:
        """Parser Method"""
        pass
    
    @abc.abstractmethod
    def parse_body(self) -> List[str]:
        """Parser Method"""
        pass

class SQLLiteRequest():
    def __init__(self, config: dict):
        if self.validate_request(config):
            self.is_valid = True
            self.table = config['table']
            self.start_date = config['startDate']
            self.Asset = config['asset']        
    
    @staticmethod
    def validate_request(config: dict) -> bool:
        try:
            config['table']
            config['startDate']
            config['asset']
            return True
        except:
            return False        


class SqlLiteConnection(Connection):
    def __init__(self, datasource):
        self.config = datasource # "data/prod.db"

    def load_data_source(self):
        """Open Database Connection"""
        self.database = sqlite3.connect
       
    def read_table(self, request: dict) -> dict: # TODO pass error messages forward
        """Takes Request and generates sql commands - obviously here just simplified"""                
        
        try:            
            with self.database(self.config) as conn:
                conn.row_factory = sqlite3.Row
                
                read_request = SQLLiteRequest(request)
                if read_request.is_valid != True:
                    raise ValueError('Invalid SQLLite Request') 
                
                # Here over-simplified sql code generation, didn't want to over do it here
                query = "SELECT * FROM " + read_request.table + " a WHERE a.start_date >= ? AND a.asset_name = ?"
                return [dict(row) for row in conn.execute(query, (read_request.start_date,read_request.Asset,)).fetchall()]
                   
                
        except sqlite3.Error as e:
            pdb.set_trace()
            print(e)
        except ValueError as e:
            pdb.set_trace()
            print(e)
            
        return {}
                  
class TextFileParser(Parser):
    def __init__(self, datasource):
        self.config = datasource # "data/text_file.txt"
        self.text = {}

    def load_data_source(self):
        """Load File into Memory"""
        # TODO pass error messages forward
        with open(self.config, 'r') as file:
            paragraph = []
            lines = file.readlines()
            p = 1
            for line in lines:
                # Create Dictionary of Paragraphs with Header Separated to find it easier later on
                if p == 1:
                    self.text['header'] = line.strip()
                    p = p+1
                    continue                    
                elif line != '\n':
                    paragraph.append(line.strip())
                    continue
                else:
                    self.text[p] = paragraph
                    p = p+1   
                    paragraph = []

    def parse_header(self) -> str:
        return self.text['header']
        
    def parse_body(self) -> List[str]:
        return [value for key, value in self.text.items() if key not in ['header', '']]