from typing import Literal

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from config import llm
from state import StackState
from agents.prompts import ORCHESTRATOR_PROMPT


class RouteDecision(BaseModel):
    agents: list[
        Literal["menu_agent", "order_agent"]
    ] = Field(
        description="The specialist agents that should handle the request."
    )

    reasoning: str = Field(
        description="Brief explanation for why these agents were selected."
    )


router_llm = llm.with_structured_output(RouteDecision)


def orchestrator_node(state: StackState):
    messages = [
        SystemMessage(content=ORCHESTRATOR_PROMPT),
        HumanMessage(content=state["user_query"]),
    ]

    decision = router_llm.invoke(messages)

    return {
        "route": decision.agents
    }