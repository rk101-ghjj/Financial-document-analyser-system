## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier
from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=(
        "Analyze the uploaded financial document at {file_path} to answer the user's question: {query}. "
        "Extract key sections (overview, revenue, margins, cash flow, guidance, risks) and summarize them succinctly. "
        "Base all claims on the document content and note any assumptions."
    ),
    expected_output=(
        "JSON with fields: summary, key_metrics, risks, insights, citations (page/section refs)."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Using the extracted content from {file_path}, outline investment considerations relevant to: {query}. "
        "Discuss potential upside/downside drivers, catalysts, and uncertainties. Include a disclaimer."
    ),
    expected_output=(
        "Bulleted considerations: thesis, catalysts, watch items, and neutral tone disclaimer."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "From the document at {file_path}, identify key risk factors (market, execution, liquidity, regulatory) "
        "and summarize plausible mitigations. Align to the user's context: {query}."
    ),
    expected_output=(
        "Short list of risks with brief rationale and mitigation ideas."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

    
verification = Task(
    description=(
        "Verify that the file at {file_path} is a financial document (e.g., earnings release, 10-Q, presentation). "
        "If yes, list detected sections and a one-line summary for each."
    ),
    expected_output=(
        "Boolean is_financial, sections list, and brief rationale."
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)