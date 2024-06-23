import pdb
import abc
import pandas as pd
from typing import List
from dataclasses import dataclass

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
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
    
class StandardReportPdf(ReportTemplate):
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font = 'Times-Roman'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
       
    def format_document(self):
        pass

class SimpleReportPdf(ReportTemplate):
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.font = 'Times-Roman'
        self.header_style = self.styles['Heading1']
        self.body_style = self.styles['Normal']
       
    def format_document(self):
        pass

@dataclass
class ReportRequest:
    name: str
    client: int
    type: str
    start_date: str
    restrictions: dict
    template: ReportTemplate
    debug: bool

class ReportGenerator():
    def __init__(self, report_request: ReportRequest):
        self.canvas = Canvas(report_request.name, pagesize=report_request.template.page_size)
        self.report_template = report_request.template
                
    def generate_report(self):
        match self.report_template:
            case SimpleReportPdf():
                return "Bad request"
            case StandardReportPdf():
                 return "Bad request"
            case _:
                return "Something's wrong with the internet"
    
    

# styles = getSampleStyleSheet()
# styleN = styles['Normal']
# styleH = styles['Heading1']
# story = []

# #add some flowables
# story.append(Paragraph("This is a Heading",styleH))
# story.append(Paragraph("This is a paragraph in <i>Normal</i> style.",
#     styleN))
# c  = Canvas('mydoc.pdf')
# f = Frame(inch, inch, 6*inch, 9*inch, showBoundary=1)
# f.addFromList(story,c)
# c.save()

# self.canvas.saveState()
# self.canvas.setFont('Times-Bold',16)
# self.canvas.drawCentredString(PAGE_WIDTH/2.0, defaultPageSize[1]-108, Title)
# self.canvas.setFont('Times-Roman',9)
# self.canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
# self.canvas.restoreState()