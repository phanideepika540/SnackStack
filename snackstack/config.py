import os
import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from openai import OpenAI


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


# Direct OpenAI SDK client
openai_client = OpenAI(
    api_key=OPENAI_API_KEY
)


# Chat model used by the agents
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    api_key=OPENAI_API_KEY,
)


# Embedding model used by the menu RAG system
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY,
)


def get_logger(name: str) -> logging.Logger:
    """
    Return a logger for the given module/component.
    """
    return logging.getLogger(name)