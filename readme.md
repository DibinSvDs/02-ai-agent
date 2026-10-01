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
                         │      LLM      │
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

## 🗄️ Data

For simplicity, the employee information and leave balances are currently stored directly inside `tools.py`.

For example:

```python
employees = {
    "EMP001": {
        "name": "John",
        "department": "Data Science",
        "role": "Data Scientist"
    },
    "EMP002": {
        "name": "Sarah",
        "department": "Human Resources",
        "role": "HR Manager"
    }
}
```

The leave balances are also stored inside `tools.py`:

```python
leave_balances = {
    "EMP001": 12,
    "EMP002": 18
}
```

This keeps the project intentionally simple so the focus remains on understanding **LLM tool calling and the agent loop**.

In a real enterprise application, this data could later be moved to a database, API, or other external data source.

---

## 🔄 Example Agent Flow

Suppose the user asks:

```text
Tell me EMP002's department and how many days of leave they have.
```

This question requires information from **two different tools**.

### Step 1 — User asks a question

```text
Tell me EMP002's department and how many days of leave they have.
```

### Step 2 — Qwen receives the question and available tools

Qwen determines that it needs employee information first.

Conceptually:

```text
Tool: get_employee_info

Arguments:
employee_id = EMP002
```

### Step 3 — Python executes the selected tool

```python
get_employee_info("EMP002")
```

### Step 4 — The tool returns data

```text
{
    "name": "Sarah",
    "department": "Human Resources",
    "role": "HR Manager"
}
```

### Step 5 — The result is sent back to Qwen

Qwen now knows the department but still needs the leave balance.

It decides to call another tool:

```text
Tool: check_leave_balance

Arguments:
employee_id = EMP002
```

### Step 6 — Python executes the second tool

```python
check_leave_balance("EMP002")
```

The tool returns:

```text
EMP002 has 18 days of leave remaining.
```

### Step 7 — Qwen generates the final answer

```text
EMP002 is in Human Resources and has 18 days of leave remaining.
```

This demonstrates the **agent loop**:

```text
User
  ↓
Qwen3
  ↓
Tool
  ↓
Tool Result
  ↓
Qwen3
  ↓
Another Tool
  ↓
Tool Result
  ↓
Qwen3
  ↓
Final Answer
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
│       Contains the Python tool functions and
│       the sample employee/leave data used by them.
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
What can I help you with? Tell me EMP002's department and how many days of leave they have.
```

The application will show:

* Qwen3's thinking
* Tool calls
* Tool arguments
* Tool results
* Final answer

Example:

```text
--- Qwen Thinking ---

The user needs the employee's department and leave balance.
I need to retrieve the employee information first.

--- Tool Call ---

Tool: get_employee_info
Arguments: {'employee_id': 'EMP002'}

--- Tool Result ---

{'name': 'Sarah',
 'department': 'Human Resources',
 'role': 'HR Manager'}

--- Qwen Thinking ---

I have the department information.
I still need to check the employee's leave balance.

--- Tool Call ---

Tool: check_leave_balance
Arguments: {'employee_id': 'EMP002'}

--- Tool Result ---

EMP002 has 18 days of leave remaining.

--- Final Answer ---

EMP002 is in Human Resources and has 18 days of leave remaining.
```

The exact Qwen3 thinking output may differ between runs.

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
* How an agent can call multiple tools sequentially
* The difference between an LLM application and an agent
* How the agent loop works
* How an LLM can decide what action to take instead of relying on hard-coded Python rules

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
Decide again
  ↓
Another Tool OR Final Answer
```

The main purpose of an agent is to **decide and take actions using tools**.

---

## 🚀 Future Improvements

This project is intentionally kept simple to understand the underlying mechanics before introducing agent frameworks.

Planned improvements include:

* Better error handling
* Tool-call validation
* Conversation memory
* Move employee data to SQLite
* Connect to PostgreSQL
* Connect tools to REST APIs
* More realistic enterprise tools
* Agentic RAG
* LangGraph implementation
* Agent tracing and evaluation
* Production deployment

---

## 📚 Learning Path

This project is part of a hands-on AI engineering learning path:

```text
01 — RAG
      ↓
02 — AI Agent
      ↓
03 — Agentic RAG
      ↓
04 — Agentic AI
      ↓
Production AI Systems
```

The projects are intentionally built from the fundamentals first, before introducing frameworks such as **LangChain** and **LangGraph**.
