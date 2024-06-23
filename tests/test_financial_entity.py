import pytest
import pdb
from pcapp import financial_entity
from pcapp import report_generator
from pcapp.report_request import ReportRequest, ReportType

class TestFinancialEntity:
    def test_types(test):
        newRequest = ReportRequest("Test.pdf", 1, "performance", "2022-01-01", "wind thingy",  ReportType.StandardReportPdf, True)
        
        emptyTable = financial_entity.Table(newRequest)
        emptyText = financial_entity.Text(newRequest)
              
        assert isinstance(emptyTable, financial_entity.FinancialEntity)
        assert isinstance(emptyText, financial_entity.FinancialEntity)
        
    def test_table_request(test):
        newRequest = ReportRequest("Test.pdf", 1, "performance", "2022-01-01", "wind thingy",  ReportType.StandardReportPdf, True) 
        newTable = financial_entity.Table(newRequest)
        newTable.process_request()
        assert newTable.processed_request['table'] == 'monthly_performance'
        assert newTable.processed_request['startDate'] == '2022-01-01'
        assert newTable.processed_request['asset'] == 'Wind Turbine Park'
        
    def test_table(test):   
        newRequest = ReportRequest("Test.pdf", 1, "performance", "2022-01-01", "wind thingy",  ReportType.StandardReportPdf, True)
        
        newTable = financial_entity.Table(newRequest)
        newTable.request_data()
        assert len(newTable.imported_table) == 3
        newTable.process_data()
        assert len(newTable.processed_table.columns) == 5      
        
    def test_text(test):
        newRequest = ReportRequest("Test.pdf", 1, "performance", "2022-01-01", "wind thingy",  ReportType.StandardReportPdf, True) 
        
        newText = financial_entity.Text(newRequest)
        newText.request_data()
        newText.process_data()
        assert newText.processed_header == "Why Americans aren’t buying more EVs"
        assert len(newText.processed_body) == 55