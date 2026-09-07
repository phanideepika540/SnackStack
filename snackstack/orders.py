import json
from pathlib import Path
from datetime import datetime
import uuid


ORDERS_FILE = Path(__file__).parent / "orders.json"
from pydantic import BaseModel, Field
from typing import Literal


class OrderItem(BaseModel):
    menu_item_id: str = Field(
        description="The ID of the menu item being ordered"
    )
    quantity: int = Field(
        gt=0,
        description="Number of units of the menu item"
    )


class Order(BaseModel):
    order_id: str = Field(
        description="Unique identifier for the order"
    )
    customer_id: str = Field(
        description="Unique identifier for the customer"
    )
    items: list[OrderItem] = Field(
        min_length=1,
        description="Items included in the order"
    )
    status: Literal[
        "PLACED",
        "PREPARING",
        "READY",
        "DELIVERED",
        "CANCELLED"
    ] = "PLACED"
    created_at: str = Field(
        description="Timestamp when the order was created"
    )
class CreateOrderRequest(BaseModel):
    customer_id: str
    item_id: str
    quantity: int
def load_orders():
    """Load all orders from orders.json."""
    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_orders(orders):
    """Save all orders to orders.json."""
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=2)



def create_order(customer_id: str, items: list):
    """Create a new order."""

    orders = load_orders()

    order = {
        "order_id": f"ORD-{uuid.uuid4().hex[:8].upper()}",
        "customer_id": customer_id,
        "items": items,
        "status": "PLACED",
        "created_at": datetime.now().isoformat(),
    }

    orders.append(order)

    save_orders(orders)

    return order


def update_order_status(order_id: str, status: str):
    """Update the status of an existing order."""

    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = status
            save_orders(orders)
            return order

    return None


def cancel_order(order_id: str):
    """Cancel an existing order."""

    orders = load_orders()

    for order in orders:
        if order["order_id"] == order_id:

            if order["status"] in ["DELIVERED", "CANCELLED"]:
                return None

            order["status"] = "CANCELLED"

            save_orders(orders)

            return order

    return None