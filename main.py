#!/usr/bin/ python3

from pcapp.report_controller import ReportController

from flask import Flask
from flask import request

app = Flask(__name__)
            
@app.route("/reportgenerator", methods=['GET'])
def report_api():
    RunReport = ReportController()
    RunReport.handle_request_flask(request.json)
    return "Report Generation Complete"

# Without Flask
# request = '"request_name": "Monthly Report", "client": "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01"'
# RunReport = ReportController()
# RunReport.handle_request(request)

# With Flask
# flask --app main run --debug
# curl -XGET -H "Content-type: application/json" -d '{"request_name": "Monthly Report", client: "1", "report_template": "standard", "report_metric": "performance", "asset_restrictons": "wind", "start": "2022-01-01"}' 'http://127.0.0.1:5000/reportgenerator'

