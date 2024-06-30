import abc

from pcapp import financial_entity
from pcapp.report_request import ReportRequest, ReportType

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

import pdb

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
    """Standard Report has Text and a Table"""
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font_body = 'Times-Roman'
        self.font_header = 'Times-Bold'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
        
    def format_document(self, request: ReportRequest):    
        """Standard Report Formatting"""
        document = SimpleDocTemplate(request.name)
        story = []
        title = Paragraph(self.text.processed_header, self.header_style)
        story.append(title)
        story.append(Spacer(1,1*cm))        
        
        datatable = [self.table.processed_table.columns[:,].values.astype(str).tolist()] + self.table.processed_table.values.tolist()

        table = Table(datatable)
        story.append(table)
        story.append(Spacer(1,1*cm))  
        
        for t in list(self.text.processed_body):
            if t == []:
                continue
            
            p = Paragraph(t[0], self.body_style)
            story.append(p)
            story.append(Spacer(1,0.4*cm))
        
        if request.debug:
            document.build(story)
            
        return document, story
       
    def process_content(self, request: ReportRequest):
        """Get necessary content for standard report"""
        text, table = financial_entity.Text(request), financial_entity.Table(request)
        
        text.request_data()
        text.process_data()

        try:
            table.request_data()
        except Exception: 
            raise        
        table.process_data()
        
        self.text = text
        self.table = table
               

class SimpleReportPdf(ReportTemplate):
    """Simple Report is Just Text"""
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font = 'Times-Roman'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
       
    def format_document(self, request: ReportRequest):        
        """Formatting for simple report"""
        document = SimpleDocTemplate(request.name)
        story = []
        title = Paragraph(self.text.processed_header, self.header_style)
        story.append(title)
        story.append(Spacer(1,1*cm))
        for t in list(self.text.processed_body):
            if t == []:
                continue
            
            p = Paragraph(t[0], self.body_style)
            story.append(p)
            story.append(Spacer(1,0.4*cm))
        
        if request.debug:
            document.build(story)
     
        return document, story
    
    def process_content(self, request: ReportRequest):
        """Content for Simple Report"""
        text = financial_entity.Text(request)
        
        text.request_data()
        text.process_data()       
        self.text = text



class ReportGenerator():
    """Class that determins the report type and handles output"""
    def __init__(self, report_request: ReportRequest):        
        self.request = report_request
                
    def generate_report(self):        
        
        match self.request.template:
            case ReportType.SimpleReportPdf:                
                self.report = SimpleReportPdf()                
                self.report.process_content(self.request)
                if ".pdf" not in self.request.name:
                    self.request.name = self.request.name+".pdf"
                                
            case ReportType.StandardReportPdf:
                self.report = StandardReportPdf()                
                self.report.process_content(self.request)
                if ".pdf" not in self.request.name:
                    self.request.name = self.request.name+".pdf"  
                    
            case _:
                pdb.set_trace()
                raise ValueError('Missing report template in request') 
        
        self.document, self.content = self.report.format_document(self.request)
        
        if self.request.debug != True:
            self.document.build(self.content)
        