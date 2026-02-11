import os
import operator
import sys
import requests
from typing import Annotated, TypedDict, Union

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Ensure we can import locally
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from clickup import ClickUpClient

# Load Env
from dotenv import load_dotenv
load_dotenv()

CLICKUP_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- 1. Tools ---
clickup_client = ClickUpClient(CLICKUP_KEY)

@tool
def create_lead_task(name: str, phone: str, intent: str, details: str):
    """Creates a lead task in ClickUp and reports to Local Dashboard."""
    data = {"name": name, "phone": phone, "intent": intent, "original_text": details}
    
    backend_url = os.getenv("BACKEND_URL", "http://backend:5001")
    try:
        requests.post(f"{backend_url}/api/webhook/lead", json=data, timeout=2)
    except Exception as e:
        print(f"Local dashboard sync failed: {e}")

    # 2. Save to ClickUp
    if not CLICKUP_LIST_ID:
        return f"Lead '{name}' saved to Dashboard, but ClickUp List ID is not configured."
    
    result = clickup_client.create_task(CLICKUP_LIST_ID, data)
    if result:
        return f"Lead '{name}' successfully created in ClickUp and Dashboard."
    else:
        return f"Lead '{name}' saved to Dashboard, but ClickUp API failed (Check keys)."

# --- 2. State & Graph ---

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

# Initialize LLM
llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    openai_api_key=OPENROUTER_API_KEY, 
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0,
    default_headers={
        "HTTP-Referer": "http://localhost:8080",
        "X-Title": "Real Estate Lead Bot",
    }
) if OPENROUTER_API_KEY else None

if llm:
    llm_with_tools = llm.bind_tools([create_lead_task])

async def call_model(state: AgentState):
    messages = state['messages']
    if not llm:
        return {"messages": [AIMessage(content="Error: OPENROUTER_API_KEY missing.")]}
    
    # SYSTEM PROMPT: Conversational Agent Logic
    system_prompt = """You are a professional Real Estate Assistant for a premium agency.

YOUR GOAL:
Engage the user in a natural conversation to understand their needs. Do NOT create a lead immediately. You must gather the following THREE pieces of information:

1. **Name**: The user's name.
2. **Phone Number**: A valid contact number.
3. **Intent/Requirement**: Specific details about what they are looking for (e.g., "Buying a 3-bed villa in Dubai Hills", "Renting a studio in Marina", "Selling my property").

RULES:
- If the user says "Hi" or "Hello", greet them warmly and ask how you can assist them with their real estate needs.
- If the user provides partial info (e.g., just "I want to buy"), ask follow-up questions (e.g., "Great! What location are you interested in?" or "What is your budget?").
- ONLY when you have ALL three pieces of information (Name, Phone, Intent), call the `create_lead_task` tool.
- If the user asks general questions, answer them helpfuly.
- Be polite, professional, and concise.
"""
    
    system_message = SystemMessage(content=system_prompt)
    if not isinstance(messages[0], SystemMessage):
        messages = [system_message] + messages
        
    try:
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}
    except Exception as e:
        print(f"!!! AI Agent Error: {e}")
        return {"messages": [AIMessage(content=f"Error: The AI model failed to respond. (Detail: {str(e)[:100]}...)")]}

def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Construct Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode([create_lead_task]))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

app = workflow.compile()
