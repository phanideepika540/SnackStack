
import logging

from langchain_core.messages import SystemMessage

from config import llm
from state import StackState

from tools.order_tools import (
    place_order,
    change_order_status,
    cancel_existing_order,
)

from tools.rag import (
    search_order_knowledge_base,
)

# ---------------------------------------------------------
# Logger
# ---------------------------------------------------------

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Order Agent Tools
# ---------------------------------------------------------

ORDER_TOOLS = [
    search_order_knowledge_base,
    place_order,
    change_order_status,
    cancel_existing_order,
]


# ---------------------------------------------------------
# Order LLM
# ---------------------------------------------------------

order_llm = llm.bind_tools(ORDER_TOOLS)


# ---------------------------------------------------------
# Order Agent
# ---------------------------------------------------------

def order_agent(state: StackState):

    logger.info("Order Agent started")

    messages = state["messages"]

    logger.debug(
        "Order Agent received %d messages",
        len(messages)
    )

    response = order_llm.invoke(
        [
            SystemMessage(
                content="""
You are the SnackStack Order Agent.

Your responsibility is to help users with their
food orders.

Use search_order_knowledge_base() when you need
to retrieve information about existing orders,
customers, order status, delivery, tracking,
or order history.

Use place_order() when the user wants to create
a new order.

Use change_order_status() when the user explicitly
requests a change to an order's status.

Use cancel_existing_order() when the user wants
to cancel an existing order.

Do not invent order information.

Do not assume an order ID or customer ID that the
user has not provided.

For questions about existing orders, use the order
knowledge base rather than trying to infer the answer.

For actions such as placing, cancelling, or changing
an order, use the appropriate transactional tool.

After receiving a tool result, use it to determine
whether another tool call is necessary or whether
you can provide the final response.
""".strip()
            ),
            *messages,
        ]
    )

    # -----------------------------------------------------
    # Log LLM decision
    # -----------------------------------------------------

    if response.tool_calls:

        logger.info(
            "Order Agent requested %d tool call(s)",
            len(response.tool_calls)
        )

        for tool_call in response.tool_calls:

            logger.info(
                "Tool selected: %s",
                tool_call["name"]
            )

            logger.debug(
                "Tool arguments: %s",
                tool_call["args"]
            )

    else:

        logger.info(
            "Order Agent generated final response"
        )

    return {
        "messages": [response],
        "order_response": response.content
    }
