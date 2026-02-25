from crewai import Task

class FinancialTasks:
    def analysis_task(self, agent):
        return Task(
            description="""Analyze the Tesla Q2 2025 document. Extract:
            1. Total Revenue and Net Income.
            2. Vehicle delivery numbers.
            3. Mentioned operational risks.""",
            expected_output="A structured markdown table with key financial metrics and a list of risks.",
            agent=agent
        )

    def recommendation_task(self, agent):
        return Task(
            description="""Review the analysis. Based on the growth and risks,
            provide a final investment outlook and a 3-sentence summary.""",
            expected_output="A summary report including a recommendation (Buy/Hold/Sell) and rationale.",
            agent=agent
        )
