from pcapp.report_request import ReportRequest, ReportType
from pcapp import report_generator
from flask import Request
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
    """Report Controller handles requests from all sources but does not expose the application directly"""
    def __init__(self):
        pass
    
    @staticmethod
    def handle_request_parse(user_input: str):
        """Request handling for hard coded requests in python using a structured json-like string"""
        input = json.loads(user_input)
        
        template = TEMPLATE_MAPPING[input["report_template"]]
        
        try:
            debug = input["debug"].lower == "true"
        except KeyError:
            debug = False
 
        newRequest = ReportRequest(name = input["request_name"], 
                                   client= int(input["client"]), 
                                   template= template, 
                                   type= input["report_metric"], 
                                   restrictions= input["asset_restrictons"], 
                                   start_date= input["start"]    , 
                                   debug=debug)  
        
        newReport = report_generator.ReportGenerator(newRequest)      
        newReport.generate_report()

    @staticmethod
    def handle_request_flask(request: dict):
        """Takes the structured json from the flask enpoint and passes it to the application"""
        template = TEMPLATE_MAPPING[request["report_template"]]
 
        try:
            debug = request["debug"].lower == "true"
        except KeyError:
            debug = False
        
        newRequest = ReportRequest(name = request["request_name"], 
                                   client= int(request["client"]), 
                                   template= template, 
                                   type= request["report_metric"], 
                                   restrictions= request["asset_restrictons"], 
                                   start_date= request["start"]    , 
                                   debug=debug)  
        
        newReport = report_generator.ReportGenerator(newRequest)      
        newReport.generate_report()


