from pcapp.report_request import ReportRequest, ReportType
from pcapp import report_generator
import pdb

import json


# User input should be structured in some manner, otherwise we can plug in an llm and try and decifer what they say
# e.g. lets go with something like "request_name: "Monthly Report", client: "1", report_template: "standard", report_metric: "performance", asset_restrictons: "wind", start: "2022-01-01"

TEMPLATE_MAPPING = {
    "standard": ReportType.StandardReportPdf,
    "standard report": ReportType.StandardReportPdf,
    "simple": ReportType.SimpleReportPdf,
    "simple report": ReportType.SimpleReportPdf
}

class ReportController():
    def __init__(self):
        pass
    
    @staticmethod
    def handle_request(user_input: str):
        
        input = json.loads(user_input)
        
        template = TEMPLATE_MAPPING[input["report_template"]]
 
        newRequest = ReportRequest(name = input["request_name"], 
                                   client= int(input["client"]), 
                                   template= template, 
                                   type= input["report_metric"], 
                                   restrictions= input["asset_restrictons"], 
                                   start_date= input["start"]    , 
                                   debug=input["debug"].lower == "true")  
        
        newReport = report_generator.ReportGenerator(newRequest)      
        newReport.generate_report()
       