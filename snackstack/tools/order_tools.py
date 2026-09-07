from langchain_core.tools import tool

from orders import (
    create_order,
    update_order_status,
    cancel_order,
    CreateOrderRequest,
)


@tool
def place_order(request: CreateOrderRequest):
    """Create a new food order for a customer."""
    return create_order(request)


@tool
def change_order_status(order_id: str, status: str):
    """Update the status of an existing order."""
    return update_order_status(order_id, status)


@tool
def cancel_existing_order(order_id: str):
    """Cancel an existing order."""
    return cancel_order(order_id)