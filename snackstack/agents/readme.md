# 🍔 SnackStack

An AI-powered food ordering assistant built with **Python, LangChain, LangGraph, and OpenAI**.

SnackStack is a learning and portfolio project focused on building a **multi-agent, tool-using AI application** with state management, conditional routing, persistence, and voice interaction.

---

## 🚀 Overview

SnackStack allows users to interact with a food-ordering assistant using natural language.

The application uses specialized AI agents to handle different types of requests.

For example:

```text
User: What chicken dishes do you have?

        ↓

   Orchestrator
        ↓
    Menu Agent
        ↓
    Menu Tools
        ↓
   Synthesizer
        ↓
   Final Answer

   User: What is the status of my order?

        ↓

   Orchestrator
        ↓
    Order Agent
        ↓
   Order Tools
        ↓
   Synthesizer
        ↓
   Final Answer

   Architecture

SnackStack uses LangGraph to orchestrate the application workflow.
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │   Orchestrator   │
                       │                  │
                       │ Intent Routing   │
                       └────────┬─────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
             ┌─────────────┐         ┌─────────────┐
             │  Menu Agent │         │ Order Agent │
             └──────┬──────┘         └──────┬──────┘
                    │                       │
                    ▼                       ▼
             ┌─────────────┐         ┌─────────────┐
             │ Menu Tools  │         │ Order Tools │
             └──────┬──────┘         └──────┬──────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Synthesizer    │
                       │                  │
                       │ Final Response   │
                       └────────┬─────────┘
                                │
                                ▼
                         ┌───────────────┐
                         │     User      │
                         └───────────────┘
                         "What is on the menu?"
                                ↓
                            Menu Agent
                            "Where is my order?"
                                ↓
                            Order Agent
                            User:
                            Do you have Butter Chicken?
                            🤖 Agents
1. Orchestrator

The Orchestrator is responsible for determining which specialist agent should handle the user's request.

Example:

Orchestrator:
→ Menu Agent

Menu Agent:
→ Menu Tool

Menu Tool:
→ Butter Chicken found

Menu Agent:
→ Response

Synthesizer:
→ Final response
2. Menu Agent

The Menu Agent handles menu-related requests.

Examples:

Search menu items
Find dishes
Get prices
Check menu availability
Answer questions about menu items

Example:

User:
Do you have Butter Chicken?

Orchestrator:
→ Menu Agent

Menu Agent:
→ Menu Tool

Menu Tool:
→ Butter Chicken found

Menu Agent:
→ Response

Synthesizer:
→ Final response
3. Order Agent

The Order Agent handles order-related requests.

Examples:

Check order status
Create an order
Modify an order
Cancel an order
Retrieve order information

Example:

User:
What is the status of ORD-201?

Orchestrator:
→ Order Agent

Order Agent:
→ Order Tool

Order Tool:
→ Retrieves order

Order Agent:
→ Response

Synthesizer:
→ Final response
4. Synthesizer

The Synthesizer is responsible for producing the final response to the user.

The specialist agent places its response into graph state.

The Synthesizer then selects the available specialist response.

For example:

specialist_response = (
    menu_response
    or order_response
)

This reflects the current architecture where the Orchestrator sends a request to one specialist agent.

🔄 Agent + Tool Loop

Agents can call tools when they need additional information.

The workflow can look like:

                ┌───────────────┐
                │     Agent     │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │      LLM      │
                └───────┬───────┘
                        │
                 Need a tool?
                    /       \
                  Yes        No
                   │          │
                   ▼          ▼
              ┌────────┐   Final Answer
              │  Tool  │
              └────┬───┘
                   │
                   ▼
              Tool Result
                   │
                   └──────────► Agent

This allows the agent to dynamically decide when it needs external information.

🧠 Graph State

SnackStack uses a shared state object to pass information between LangGraph nodes.

Conceptually:

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_query: str

    menu_response: str
    order_response: str

The state provides a common communication mechanism between nodes.

💾 Persistence

SnackStack uses LangGraph checkpointing to maintain graph state across interactions.

This allows the application to support conversational workflows.

For example:

User:
What is the status of my order?

Assistant:
Your order is out for delivery.

User:
What was my previous question?

Assistant:
You asked about your order status.

The goal is to allow the graph to maintain useful conversation state instead of treating every request as completely independent.

🎙️ Voice Interaction

SnackStack also includes voice input and output.

The conceptual workflow is:

        User Speech
             │
             ▼
    Speech Recognition
             │
             ▼
        User Query
             │
             ▼
        LangGraph
             │
             ▼
      Final Response
             │
             ▼
      Text-to-Speech
             │
             ▼
        User Audio

This allows SnackStack to evolve from a text-based assistant into a conversational voice assistant.

🛠️ Technology Stack
Technology	Purpose
Python	Application development
LangGraph	Agent orchestration and state management
LangChain	LLM and tool integration
OpenAI	Large Language Model
Pydantic	Structured data validation
JSON	Menu and order data
python-dotenv	Environment configuration
LangGraph Checkpointer	Conversation persistence
📁 Project Structure
snackstack/
│
├── agents/
│   ├── __init__.py
│   ├── orchestrator.py
│   ├── menu_agent.py
│   ├── order_agent.py
│   └── synthesizer.py
│
├── tools/
│   ├── __init__.py
│   ├── menu_tools.py
│   └── order_tools.py
│
├── state/
│   ├── __init__.py
│   └── state.py
│
├── data/
│   ├── menu.json
│   └── orders.json
│
├── config.py
├── voice.py
├── main.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
⚙️ Installation
1. Clone the repository
git clone <your-repository-url>
cd snackstack
2. Create a virtual environment
python -m venv .venv
Windows
.venv\Scripts\activate
macOS / Linux
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
🔑 Configuration

Create a .env file in the project root.

OPENAI_API_KEY=your-api-key

The .env file should not be committed to Git.

Use .env.example as a template:

OPENAI_API_KEY=
▶️ Running the Application

Start SnackStack with:

python main.py
💬 Example Conversations
Menu Request
User:
What vegetarian items are available?

Assistant:
We have several vegetarian options...
Order Request
User:
Check the status of ORD-201.

Assistant:
Your order is currently Out for Delivery.
Conversational Request
User:
What is the status of my order?

Assistant:
Your order is out for delivery.

User:
When did I place it?

Assistant:
You placed the order earlier today.
🎯 Learning Objectives

SnackStack is designed to demonstrate practical Agentic AI concepts.

The project explores:

Large Language Models
LangChain
LangGraph
Graph-based workflows
Multi-agent architecture
Conditional routing
Shared graph state
Tool calling
Agent/tool execution loops
Structured outputs
Pydantic models
Conversation memory
Checkpointing
Voice AI
Environment configuration
🔮 Future Enhancements

The architecture can be extended with additional agents and capabilities.

Planned
 Customer Agent
 Recommendation Agent
 Payment Agent
 Inventory Agent
 Database persistence
 Long-term memory
 Streaming responses
 Human-in-the-loop approval
 Authentication
 LangSmith observability
 REST API
 Web interface
 Mobile interface
Multi-Agent Routing

The current implementation routes to one specialist.

A future version could support requests requiring multiple agents.

For example:

User:
Show me vegetarian dishes and add paneer tikka to my order.

                    │
                    ▼
              Orchestrator
                    │
             ┌──────┴──────┐
             ▼             ▼
        Menu Agent     Order Agent
             │             │
             └──────┬──────┘
                    ▼
               Synthesizer
                    │
                    ▼
               Final Answer
📚 Why SnackStack?

SnackStack is intentionally designed as more than a simple chatbot.

The project demonstrates how traditional software engineering concepts can be combined with modern AI:

Traditional Software
        +
LLMs
        +
Tools
        +
State
        +
Graph Orchestration
        =
Agentic AI Application
👩‍💻 Project Status

🚧 Work in Progress

SnackStack is continuously evolving as new Agentic AI concepts are explored and implemented.

⭐ Key Concept

The core idea behind SnackStack is:

Don't build one giant AI prompt. Build a system of specialized agents, tools, state, and orchestration.

User
 ↓
Orchestrator
 ↓
Specialist Agent
 ↓
Tools
 ↓
State
 ↓
Synthesizer
 ↓
User