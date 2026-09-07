import logging

from langchain_core.messages import SystemMessage

from config import llm
from state import StackState
from tools.rag import search_menu_knowledge_base


logger = logging.getLogger(__name__)


MENU_TOOLS = [
    search_menu_knowledge_base,
]

menu_llm = llm.bind_tools(MENU_TOOLS)


def menu_agent(state: StackState):

    logger.info("Menu Agent started")

    messages = state["messages"]

    logger.debug(
        "Menu Agent received %d messages",
        len(messages)
    )

    response = menu_llm.invoke(
        [
            SystemMessage(
                content="""
You are the SnackStack Menu Agent.

Your responsibility is to help users discover and
understand menu items.

Use search_menu_knowledge_base() whenever you need
information from the SnackStack menu.

Use the tool for questions involving:

- menu items
- food recommendations
- cuisines
- dietary preferences
- ingredients or descriptions
- prices
- ratings
- availability
- comparisons between menu items

Do not invent menu information.

If the user asks a menu-related question and the
answer requires menu information, use the tool.

After receiving tool results, use them to answer
the user clearly and concisely.

If the user asks something unrelated to the menu,
do not attempt to answer it as a menu question.
""".strip()
            ),
            *messages,
        ]
    )

    if response.tool_calls:
        logger.info(
            "Menu Agent requested %d tool call(s)",
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
        logger.info("Menu Agent generated final response")

    return {
        "messages": [response],
        "menu_response": response.content
    }