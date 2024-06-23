from dataclasses import dataclass
import enum

class ReportType(enum.Enum):
    StandardReportPdf: str = 'Standard Report'
    SimpleReportPdf: str = 'Simple Report'

@dataclass
class ReportRequest:
    name: str
    client: int
    type: str
    start_date: str
    restrictions: dict
    template: ReportType
    debug: bool