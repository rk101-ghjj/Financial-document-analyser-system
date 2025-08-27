## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()


from crewai.agents import Agent

from tools import search_tool, FinancialDocumentTool

llm = None

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Financial Analyst",
    goal="Provide accurate, compliant insights on the uploaded financial document answering: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "Experienced analyst specializing in corporate financial statements, earnings reports, and risk disclosures. "
        "Focus on evidence-based analysis, cite the document content, and avoid speculative claims."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    llm=llm,
    max_iter=3,
    max_rpm=3,
    allow_delegation=False
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Validate that the uploaded file is a financial document and summarize its sections.",
    verbose=True,
    memory=True,
    backstory=(
        "Background in financial reporting and compliance. Carefully checks document structure and content for relevance."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide balanced, risk-aware investment considerations grounded in the document and user's {query}.",
    verbose=True,
    backstory=(
        "Portfolio strategist focusing on evidence-based recommendations, disclaimers, and suitability considerations."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Risk Assessor",
    goal="Identify key risks and mitigations derived from the uploaded financial document.",
    verbose=True,
    backstory=(
        "Risk professional experienced in market, credit, and operational risk analysis." 
    ),
    llm=llm,
    max_iter=2,
    max_rpm=3,
    allow_delegation=False
)
