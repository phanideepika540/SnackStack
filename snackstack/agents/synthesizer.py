
"""
Synthesizer Agent

Takes the final response from a specialist agent and converts it
into a clean, concise user-facing response.
"""

from config import llm, get_logger

from state import StackState


logger = get_logger("synthesizer")


def synthesizer_node(state: StackState):

    logger.info("Synthesizer started")

    user_query = state.get("user_query", "")

    menu_response = state.get("menu_response", "")
    order_response = state.get("order_response", "")

    # Pick the response produced by the specialist agent
    specialist_response = (
        menu_response
        or order_response
    )

    if not specialist_response:

        logger.warning(
            "No specialist response found for synthesizer"
        )

        return {
            "final_answer": (
                "I'm sorry, I wasn't able to find an answer "
                "to your request."
            )
        }

    prompt = f"""
You are the final response synthesizer for SnackStack,
an AI food ordering assistant.

Your job is to convert the specialist agent's response
into a natural, concise response for the customer.

USER REQUEST:
{user_query}

SPECIALIST RESPONSE:
{specialist_response}

Instructions:

1. Answer the user's request directly.
2. Do not mention agents, tools, routing, state, or internal processing.
3. Do not invent information.
4. Preserve important facts such as order IDs, item names,
   statuses, prices, and dates.
5. Keep the response conversational and concise.
6. If the specialist response already sounds natural,
   you may simply clean it up.
7. Do not say "According to the specialist" or similar wording.

Return ONLY the final response that should be shown to the user.
"""

    try:

        response = llm.invoke(prompt)

        final_answer = response.content.strip()

        logger.info(
            "Synthesizer generated final response"
        )

        return {
            "final_answer": final_answer
        }

    except Exception:

        logger.exception(
            "Synthesizer failed"
        )

        # Safe fallback — don't lose the specialist response
        return {
            "final_answer": specialist_response
        }

