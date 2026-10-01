# 02-AI-Agent

A simple tool-using AI agent built from scratch with **Python, Ollama, and Qwen3**.

The purpose of this project is to understand the fundamentals of **AI agents and LLM tool calling** before using frameworks such as LangChain or LangGraph.

---

## 🧠 What is an AI Agent?

A traditional LLM application usually looks like:

```text
User
  ↓
LLM
  ↓
Answer
```

An AI agent can decide that it needs to perform an action before answering:

```text
User
  ↓
LLM
  ↓
Decides which tool to use
  ↓
Python executes the tool
  ↓
Tool result
  ↓
LLM
  ↓
Final answer
```

In this project, **Qwen3 makes the tool-selection decision**.

Python does not decide whether a question is about leave, employee information, or IT support. Instead, the LLM receives the available tool definitions and chooses the appropriate tool.

---

## 🏗️ Architecture

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │    QWEN3      │
                         │      LLM      │
                         └───────┬───────┘
                                 │
                         Decides which
                         tool is needed
                                 │
                                 ▼
                         ┌───────────────┐
                         │     PYTHON    │
                         │ Tool Executor │
                         └───────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
             Employee Info   Leave Balance   IT Ticket
                    │            │            │
                    └────────────┼────────────┘
                                 │
                                 ▼
                           Tool Result
                                 │
                                 ▼
                         ┌───────────────┐
                         │    QWEN3      │
                         │    LLM        │
                         └───────┬───────┘
                                 │
                                 ▼
                           Final Answer
```

---

## 🛠️ Tools

The agent currently has three tools:

### 1. `get_employee_info`

Retrieves an employee's:

* Name
* Department
* Job role

Example:

```text
get_employee_info("EMP002")
```

Result:

```text
{
    "name": "Sarah",
    "department": "Human Resources",
    "role": "HR Manager"
}
```

### 2. `check_leave_balance`

Checks how many leave days an employee has remaining.

Example:

```text
check_leave_balance("EMP002")
```

Result:

```text
EMP002 has 18 days of leave remaining.
```

### 3. `create_it_ticket`

Creates a simulated IT support ticket.

Example:

```text
create_it_ticket(
    "EMP002",
    "Laptop is not turning on"
)
```

Result:

```text
IT ticket IT-1001 created for EMP002.
Issue: Laptop is not turning on
```

These are simulated tools for learning. They do not connect to a real HR or IT system.

---

## 🔄 Example Agent Flow

Suppose the user asks:

```text
How many days of leave does EMP002 have?
```

### Step 1 — User asks a question

```text
How many days of leave does EMP002 have?
```

### Step 2 — Qwen receives the question and available tools

Qwen determines that the `check_leave_balance` tool is relevant.

Conceptually:

```text
Tool: check_leave_balance

Arguments:
employee_id = EMP002
```

### Step 3 — Python executes the selected tool

Python receives Qwen's structured tool call and executes:

```python
check_leave_balance("EMP002")
```

### Step 4 — The tool returns data

```text
EMP002 has 18 days of leave remaining.
```

### Step 5 — The result is sent back to Qwen

Qwen receives the tool result and generates the final response.

```text
EMP002 has 18 days of leave remaining.
```

---

## 📁 Project Structure

```text
02-ai-agent/
│
├── app.py
│       Main agent application.
│       Communicates with Qwen, handles tool calls,
│       executes tools, and generates the final answer.
│
├── tools.py
│       Contains the Python functions that the agent
│       is allowed to use.
│
├── requirements.txt
│       Python dependencies.
│
├── README.md
│       Project documentation.
│
└── .gitignore
        Prevents files such as the virtual environment
        from being uploaded to Git.
```

---

## 💻 Technologies

* **Python** — Application logic and tool execution
* **Ollama** — Runs the LLM locally
* **Qwen3 4B** — LLM responsible for deciding which tool to use
* **Ollama Python library** — Communication between Python and Ollama
* **Git / GitHub** — Version control

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd 02-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Git Bash:

```bash
source .venv/Scripts/activate
```

On Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Ollama

Install and run Ollama on your computer.

Then download the Qwen3 model:

```bash
ollama pull qwen3:4b
```

Make sure Ollama is running before starting the application.

---

## ▶️ Running the Agent

Run:

```bash
python app.py
```

Example:

```text
What can I help you with? How many days of leave does EMP002 have?
```

The application will show the agent's decision, tool call, tool result, and final answer.

Example:

```text
--- Qwen's Decision ---

--- Tool Call ---
Tool: check_leave_balance
Arguments: {'employee_id': 'EMP002'}

--- Tool Result ---
EMP002 has 18 days of leave remaining.

--- Final Answer ---
EMP002 has 18 days of leave remaining.
```

---

## 🎯 Learning Goals

This project focuses on understanding the fundamentals of an AI agent:

* How an LLM can use external tools
* How tools are described to an LLM
* How an LLM decides which tool to call
* How structured tool calls are generated
* How Python executes the requested tool
* How tool results are returned to the LLM
* How the LLM converts tool results into a final response
* The difference between an LLM application and an agent

---

## 🆚 RAG vs AI Agent

This project follows the RAG project in this learning series.

### RAG

```text
User
  ↓
Retrieve relevant information
  ↓
LLM
  ↓
Answer
```

The main purpose of RAG is to **retrieve relevant information** and provide it to the LLM.

### AI Agent

```text
User
  ↓
LLM
  ↓
Decide what action is needed
  ↓
Tool
  ↓
Result
  ↓
LLM
  ↓
Answer
```

The main purpose of an agent is to **decide and take actions using tools**.

---

