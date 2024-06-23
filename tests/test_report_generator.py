import pytest
import pdb
from pcapp import financial_entity
from pcapp import report_generator
from pcapp.report_request import ReportRequest, ReportType

class TestReportGenerator:
    def test_stanrdard_generator(test):
        newRequest = ReportRequest("test_standard", 1, "performance", "2022-01-01", "wind thingy", ReportType.StandardReportPdf, debug=True)
        
        newStandardReport = report_generator.StandardReportPdf()        
        newStandardReport.process_content(financial_entity.Text(newRequest), financial_entity.Table(newRequest))
        assert len(newStandardReport.table.processed_table) == 3
        
        newReport = report_generator.ReportGenerator(newRequest)
        newReport.generate_report()
            
        assert newReport.report
        
    def test_simple_generator(test):
        newRequest = ReportRequest("test_simple", 1, "performance", "2022-01-01", "wind thingy", ReportType.SimpleReportPdf, debug=True)
        newSimpleReport = report_generator.SimpleReportPdf()        
        newSimpleReport.process_content(financial_entity.Text(newRequest))
        assert len(newSimpleReport.text.processed_body) == 55
        
        newReport = report_generator.ReportGenerator(newRequest)
        newReport.generate_report()
            
        assert newReport.report