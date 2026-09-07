from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import StackState

from agents.orchestrator import orchestrator_node
from agents.menu_agent import menu_agent
from agents.order_agent import order_agent

from tools.rag import search_menu_knowledge_base
from tools.rag import search_order_knowledge_base
from langgraph.checkpoint.memory import InMemorySaver
from agents.synthesizer import synthesizer_node

from tools.order_tools import (
    place_order,
    change_order_status,
    cancel_existing_order,
)


# =========================================================
# TOOL NODES
# =========================================================

menu_tool_node = ToolNode([
    search_menu_knowledge_base,
])


order_tool_node = ToolNode([
    search_order_knowledge_base,
    place_order,
    change_order_status,
    cancel_existing_order,
])


# =========================================================
# ROUTING FUNCTIONS
# =========================================================

def route_from_orchestrator(state: StackState):
    return state["route"]


def route_from_menu_agent(state: StackState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "menu_tools"

    return "synthesizer"


def route_from_order_agent(state: StackState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "order_tools"

    return "synthesizer"


# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(StackState)


# ---------------------------------------------------------
# Add nodes
# ---------------------------------------------------------

builder.add_node("orchestrator", orchestrator_node)

builder.add_node("menu_agent", menu_agent)
builder.add_node("menu_tools", menu_tool_node)

builder.add_node("order_agent", order_agent)
builder.add_node("order_tools", order_tool_node)
builder.add_node(
    "synthesizer",
    synthesizer_node,
)


# ---------------------------------------------------------
# START → ORCHESTRATOR
# ---------------------------------------------------------

builder.add_edge(
    START,
    "orchestrator",
)


# ---------------------------------------------------------
# ORCHESTRATOR → SPECIALIST AGENT
# ---------------------------------------------------------

builder.add_conditional_edges(
    "orchestrator",
    route_from_orchestrator,
    {
        "menu_agent": "menu_agent",
        "order_agent": "order_agent",
    },
)


# ---------------------------------------------------------
# MENU AGENT → MENU TOOLS or END
# ---------------------------------------------------------

builder.add_conditional_edges(
    "menu_agent",
    route_from_menu_agent,
    {
        "menu_tools": "menu_tools",
        "synthesizer": "synthesizer",
    },
)


# ---------------------------------------------------------
# MENU TOOLS → MENU AGENT
# ---------------------------------------------------------

builder.add_edge(
    "menu_tools",
    "menu_agent",
)


# ---------------------------------------------------------
# ORDER AGENT → ORDER TOOLS or END
# ---------------------------------------------------------

builder.add_conditional_edges(
    "order_agent",
    route_from_order_agent,
    {
        "order_tools": "order_tools",
        "synthesizer": "synthesizer",
    },
)


# ---------------------------------------------------------
# ORDER TOOLS → ORDER AGENT
# ---------------------------------------------------------

builder.add_edge(
    "order_tools",
    "order_agent",
)


# =========================================================
# COMPILE
# =========================================================

checkpointer = InMemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)