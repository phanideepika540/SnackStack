from pathlib import Path

from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from data.menu import MENU_CATALOG
from data.orders import ORDERS


# =========================================================
# Configuration
# =========================================================

EMBEDDING_MODEL = "text-embedding-3-small"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# =========================================================
# Embeddings
# =========================================================

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL
)


# =========================================================
# MENU RAG
# =========================================================

def create_menu_documents() -> list[Document]:
    """Convert menu records into LangChain Documents."""

    documents = []

    for item in MENU_CATALOG:

        content = f"""
Menu Item: {item["name"]}
Category: {item["category"]}
Cuisine: {item["cuisine"]}
Price: {item["price"]}
Rating: {item["rating"]}
Dietary Tags: {", ".join(item["dietary_tags"])}
Description: {item["description"]}
Availability: {item["availability"]}
""".strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": "menu",
                    "item_id": item["id"],
                    "name": item["name"],
                },
            )
        )

    return documents


menu_vector_store = Chroma(
    collection_name="snackstack_menu",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)


def initialize_menu_rag():
    """Create menu embeddings and store them in Chroma if needed."""

    existing = menu_vector_store.get()

    if not existing["ids"]:

        documents = create_menu_documents()

        ids = [
            document.metadata["item_id"]
            for document in documents
        ]

        menu_vector_store.add_documents(
            documents=documents,
            ids=ids,
        )


menu_retriever = menu_vector_store.as_retriever(
    search_kwargs={"k": 4}
)


@tool
def search_menu_knowledge_base(query: str) -> str:
    """
    Search the SnackStack menu knowledge base using semantic
    similarity.
    """

    initialize_menu_rag()

    documents = menu_retriever.invoke(query)

    if not documents:
        return "No relevant menu information was found."

    return "\n\n---\n\n".join(
        document.page_content
        for document in documents
    )


# =========================================================
# ORDER RAG
# =========================================================

def create_order_documents() -> list[Document]:
    """Convert order records into LangChain Documents."""

    documents = []

    for order in ORDERS.values():

        content = f"""
Order ID: {order["order_id"]}
Customer: {order["customer_name"]}
Customer ID: {order["customer_id"]}
Email: {order["customer_email"]}
Item: {order["item_name"]}
Status: {order["status"]}
Order Date: {order["order_date"]}
Estimated Delivery: {order["estimated_delivery"]}
""".strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": "order",
                    "order_id": order["order_id"],
                    "customer_id": order["customer_id"],
                },
            )
        )

    return documents


order_vector_store = Chroma(
    collection_name="snackstack_orders",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR),
)


def initialize_order_rag():
    """Create order embeddings and store them in Chroma if needed."""

    existing = order_vector_store.get()

    if not existing["ids"]:

        documents = create_order_documents()

        ids = [
            document.metadata["order_id"]
            for document in documents
        ]

        order_vector_store.add_documents(
            documents=documents,
            ids=ids,
        )


order_retriever = order_vector_store.as_retriever(
    search_kwargs={"k": 4}
)


@tool
def search_order_knowledge_base(query: str) -> str:
    """
    Search the SnackStack order knowledge base using semantic
    similarity.
    """

    initialize_order_rag()

    documents = order_retriever.invoke(query)

    if not documents:
        return "No relevant order information was found."

    return "\n\n---\n\n".join(
        document.page_content
        for document in documents
    )