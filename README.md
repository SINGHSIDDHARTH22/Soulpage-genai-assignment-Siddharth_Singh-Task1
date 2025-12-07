# AI Financial Analyst Agent (Task 1)

This project implements a multi-agent workflow using **LangGraph** to perform automated financial research and analysis. It consists of two agents:
1.  **Researcher:** Searches the web for the latest financial news and stock performance.
2.  **Analyst:** Synthesizes the data into an executive summary with a Buy/Hold/Sell verdict.

## Prerequisites

1.  **Python 3.10+**
2.  **Ollama**: Ensure Ollama is installed. [Download here](https://ollama.com).

## Setup Instructions

1.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements-2.txt
    ```

2.  **Prepare the Model:**
    Open a terminal and run the following commands:
    ```bash
    ollama serve
    # In a new terminal window:
    ollama pull llama3
    ```

## How to Run

Execute the main script:
```bash
python main_task1.py
