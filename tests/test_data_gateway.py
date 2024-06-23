import pytest

from pcapp import data_gateway

class TestGateway:
    def test_types(test):
        emptyConnetion = data_gateway.SqlLiteConnection("")
        emptyFile = data_gateway.TextFileParser("")
              
        assert isinstance(emptyConnetion, data_gateway.Connection)
        assert isinstance(emptyFile, data_gateway.Parser)
        
    def test_load_text(test):
        TxtParser = data_gateway.TextFileParser("tests/test_data/test_file.txt")
        TxtParser.load_data_source()
        assert TxtParser.parse_header() == "Why Americans aren’t buying more EVs"
        
    def test_load_sqllite(test):
        dataReader = data_gateway.SqlLiteConnection("tests/test_data/test.db")
        dataReader.load_data_source()
        data = dataReader.read_table({"table": "monthly_performance", "startDate": "2022-01-01", "asset": "Wind Turbine Park"})
        assert data