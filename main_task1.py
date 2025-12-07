import sys
import requests
from typing import TypedDict
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END

def check_ollama_server():
    try:
        response = requests.get("http://localhost:11434")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False
    return False

class AgentState(TypedDict):
    company_name: str
    raw_data: str
    final_report: str

def research_node(state: AgentState):
    company = state['company_name']
    print(f"\nAgent 1 (Researcher): Searching for '{company}'...")

    try:
        search = DuckDuckGoSearchRun()
        query = f"{company} financial performance stock news analysis 2024"
        results = search.invoke(query)
        print(f"   -> Search successful.")
    except Exception as e:
        print(f"   -> Search failed. Using simulated backup data.")
        results = f"Simulated Data for {company}: Market cap stable, recent product launches successful, stock shows moderate growth."

    return {"raw_data": results}

def analyst_node(state: AgentState):
    print(f"Agent 2 (Analyst): Writing report...")
    data = state.get("raw_data")
    company = state.get("company_name")

    llm = ChatOllama(model="llama3", temperature=0)

    prompt = f"""
    You are a Senior Financial Analyst.
    Write a concise executive summary for: {company}.

    Based on this research data:
    {data}

    Format:
    - **Key Findings**
    - **Risks**
    - **Verdict** (Buy/Hold/Sell)
    """

    response = llm.invoke(prompt)
    return {"final_report": response.content}

def main():
    if not check_ollama_server():
        print("Error: Ollama server is not running.")
        print("   -> Run 'ollama serve' in a separate terminal.")
        sys.exit(1)

    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", research_node)
    workflow.add_node("analyst", analyst_node)

    workflow.set_entry_point("researcher")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", END)

    app = workflow.compile()

    print("-" * 50)
    print("AI Financial Analyst Agent")
    print("-" * 50)

    target_company = input("Enter the Company Name (e.g., Tesla, Apple): ").strip()

    if target_company:
        print(f"\nStarting Analysis for: {target_company}")
        inputs = {"company_name": target_company}

        try:
            result = app.invoke(inputs)
            print("\n" + "="*50)
            print(f"FINAL REPORT: {target_company.upper()}")
            print("="*50)
            print(result['final_report'])
        except Exception as e:
            print(f"\nError during execution: {e}")
    else:
        print("No company name entered. Exiting.")

if __name__ == "__main__":
    main()
