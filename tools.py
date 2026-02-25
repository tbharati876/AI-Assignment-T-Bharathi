get_ipython().system('pip install crewai-tools')

from crewai_tools import PDFSearchTool
import os

def get_financial_tool(pdf_path="data/sample.pdf"):
    if not os.path.exists(pdf_path):
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        print(f"Warning: {pdf_path} not found. Please upload the Tesla PDF.")

    return PDFSearchTool(pdf=pdf_path)
