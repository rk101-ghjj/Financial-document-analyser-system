## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools.tools.serper_dev_tool import SerperDevTool
from crewai_tools import PDFSearchTool
from pypdf import PdfReader

search_tool = SerperDevTool()

## Creating custom pdf reader tool
class FinancialDocumentTool:
    @staticmethod
    def read_data_tool(path='data/sample.pdf'):
        """Tool to read data from a pdf file from a path

        Args:
            path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Financial Document file
        """
        if not os.path.exists(path):
            return ""
        try:
            pdf_tool = PDFSearchTool(pdf=path)
            content = pdf_tool.extract_text()
        except Exception:
            content = ""
        if not content:
            try:
                reader = PdfReader(path)
                parts = []
                for page in reader.pages:
                    parts.append(page.extract_text() or "")
                content = "\n".join(parts)
            except Exception:
                content = ""

        content = content.replace("\r", "\n")
        while "\n\n" in content:
            content = content.replace("\n\n", "\n")
        return content.strip()

## Creating Investment Analysis Tool
class InvestmentTool:
    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> str:
        processed_data = financial_document_data or ""
        
        # Clean up the data format
        processed_data = " ".join(processed_data.split())
                
        return "Parsed document. Investment analysis module initialized."

## Creating Risk Assessment Tool
class RiskTool:
    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        return "Risk assessment module initialized."