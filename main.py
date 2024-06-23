#! /usr/bin/env python

from pcapp.report_controller import ReportController




request = '"request_name": "Monthly Report", client: "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01"'


RunReport = ReportController()
RunReport.handle_request(request)