import pytest
import sqlite3
from pcapp import data_gateway

from hypothesis import given, assume, example,settings, HealthCheck
from hypothesis import strategies as st
from unittest import TestCase

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
        
class FuzzyTestsGateway(TestCase):
    @given(address=st.text())
    def test_fuzz_load_text(self, address):
        try:
            TxtParser = data_gateway.TextFileParser(address)
            TxtParser.load_data_source()
        except FileNotFoundError:
            return

    @given(address=st.text())
    def test_fuzz_load_db(self, address):
        try:
            dataReader = data_gateway.SqlLiteConnection(address)
            dataReader.load_data_source()
            dataReader.read_table({"table": "monthly_performance", "startDate": "2022-01-01", "asset": "Wind Turbine Park"})
        except FileNotFoundError:
            return
        
    @given(param=st.text())
    def test_fuzz_db_failed_request(self, param):
        try:
            dataReader = data_gateway.SqlLiteConnection("tests/test_data/test.db")
            dataReader.load_data_source()
            dataReader.read_table({"table": param, "startDate": "2022-01-01", "asset": "Wind Turbine Park"})
        except ValueError:
            return
        except sqlite3.Error:
            return