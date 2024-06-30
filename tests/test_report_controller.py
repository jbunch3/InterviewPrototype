import pytest
import pdb


from pcapp.report_controller import ReportController

class TestReportGenerator:
    def test_stanrdard_generator(test):
        request = '{"request_name": "Monthly Report", "client": "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01", "debug": "true"}'

        RunReport = ReportController()
        RunReport.handle_request_parse(request)
        
        assert RunReport



