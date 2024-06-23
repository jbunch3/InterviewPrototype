import pdb
import abc
import pandas as pd
from typing import List
from dataclasses import dataclass

from pcapp import financial_entity
from pcapp.report_request import ReportRequest, ReportType
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas

class ReportTemplate(metaclass=abc.ABCMeta):
    """Abstract Class / Interface for Different Report Types (Print View)"""
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'format_document') and 
                callable(subclass.format_document))
    
    @abc.abstractmethod
    def format_document(self):
        """Format Document according to Report Requirements"""
        raise NotImplementedError
    
    @abc.abstractmethod
    def process_content(self):
        """process content specific to the report type"""
        raise NotImplementedError
    
class StandardReportPdf(ReportTemplate):
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font_body = 'Times-Roman'
        self.font_header = 'Times-Bold'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
        
    def format_document(self, request_name: str):        
   
        document = SimpleDocTemplate(request_name)
        Story = []
        Title = Paragraph(self.text.processed_header, self.header_style)
        Story.append(Title)
        Story.append(Spacer(1,1*cm))        
        
        datatable = [self.table.processed_table.columns[:,].values.astype(str).tolist()] + self.table.processed_table.values.tolist()

        table = Table(datatable)
        Story.append(table)
        Story.append(Spacer(1,1*cm))  
        
        for t in list(self.text.processed_body):
            if t == []:
                continue
            
            p = Paragraph(t[0], self.body_style)
            Story.append(p)
            Story.append(Spacer(1,0.4*cm))
        
        document.build(Story)
     
        return document
       
    def process_content(self, text: financial_entity.Text, table: financial_entity.Table):
        text.request_data()
        text.process_data()

        table.request_data()
        table.process_data()
        
        self.text = text
        self.table = table
               

class SimpleReportPdf(ReportTemplate):
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font = 'Times-Roman'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
       
    def format_document(self, request_name: str):        
   
        document = SimpleDocTemplate(request_name)
        Story = []
        Title = Paragraph(self.text.processed_header, self.header_style)
        Story.append(Title)
        Story.append(Spacer(1,1*cm))
        for t in list(self.text.processed_body):
            if t == []:
                continue
            
            p = Paragraph(t[0], self.body_style)
            Story.append(p)
            Story.append(Spacer(1,0.4*cm))
        
        document.build(Story)
     
        return document
    
    def process_content(self, text: financial_entity.Text):
        text.request_data()
        text.process_data()       
        self.text = text



class ReportGenerator():
    def __init__(self, report_request: ReportRequest):        
        self.request = report_request
                
    def generate_report(self):        
        
        match self.request.template:
            case ReportType.SimpleReportPdf:                
                self.report = SimpleReportPdf()                
                self.report.process_content(financial_entity.Text(self.request))
                if ".pdf" not in self.request.name:
                    self.request.name = self.request.name+".pdf"
                                
            case ReportType.StandardReportPdf:
                self.report = StandardReportPdf()                
                self.report.process_content(financial_entity.Text(self.request), financial_entity.Table(self.request))
                if ".pdf" not in self.request.name:
                    self.request.name = self.request.name+".pdf"    
        
        self.document = self.report.format_document(self.request.name)
        