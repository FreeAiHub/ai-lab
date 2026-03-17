# Project 3: AI Agent with Web Search

**Goal:** Build ReAct agent that can search the web  
**Time:** 2-3 hours  
**Stack:** Python + LangChain + Tavily API

---

## Setup

```bash
pip install langchain langchain-openai langchain-community tavily-python langchainhub

# Free Tavily API key (1000 req/month): https://tavily.com
export TAVILY_API_KEY=tvly-your-key
export OPENAI_API_KEY=sk-your-key
```

## Code: agent.py

```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from langchain.tools import tool
from datetime import datetime

# 1. LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Tools
@tool
def get_current_time() -> str:
    """Returns current date and time in Lisbon timezone"""
    return datetime.now().strftime("%Y-%m-%d %H:%M (UTC)")

search = TavilySearchResults(max_results=3)
tools = [search, get_current_time]

# 3. ReAct prompt (Thought → Action → Observation loop)
prompt = hub.pull("hwchase17/react")

# 4. Create agent
agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,   # ← See EVERY thought step! This is how agents work
    max_iterations=5
)

# 5. Test queries
queries = [
    "What are the top free AI models on OpenRouter today?",
    "What is the latest version of LangChain?",
    "What time is it now and what day of the week?",
]

for query in queries:
    print(f"\n{'='*60}")
    print(f"Question: {query}")
    result = executor.invoke({"input": query})
    print(f"\nFinal: {result['output']}")
```

## Run and observe

```bash
python agent.py
```

Watch the output carefully:
```
Thought: I need to search for...
Action: tavily_search_results_json
Action Input: "top free AI models OpenRouter"
Observation: [search results...]
Thought: Now I have the information...
Final Answer: ...
```

This is **ReAct pattern** (Reasoning + Acting) — the foundation of all AI agents.

## Add more tools

```python
@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression. Input: math expression string."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

tools = [search, get_current_time, calculate]
```

## Key concepts learned
- ReAct pattern (most important agent pattern)
- Tool definition and registration
- Agent loops and iteration limits
- Prompt engineering for agents

## ➡️ Next: [Project 4 — n8n automation](../04-n8n-email-ai/)
