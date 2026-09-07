from typing import TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated


class StackState(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]
    user_query: str
    route: list[str]
    menu_response: str
    order_response: str
    final_answer: str