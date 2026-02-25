from crewai import Agent
from __main__ import get_financial_tool

class FinancialAgents:
    def __init__(self, pdf_path):
        self.tool = get_financial_tool(pdf_path)

    def research_analyst(self):
        return Agent(
            role='Senior Financial Research Analyst',
            goal='Extract precise quarterly revenue, net income, and delivery numbers.',
            backstory="""You are a Wall Street analyst. You have a sharp eye for
            identifying year-over-year (YoY) growth and hidden financial risks in PDFs.""",
            tools=[self.tool],
            verbose=True,
            allow_delegation=False
        )

    def investment_advisor(self):
        return Agent(
            role='Chief Investment Strategist',
            goal='Provide a clear Buy/Hold/Sell recommendation based on analyst data.',
            backstory="""You specialize in long-term value investing. You translate
            raw financial data into strategic market insights for high-net-worth clients.""",
            tools=[self.tool],
            verbose=True,
            allow_delegation=True
        )
