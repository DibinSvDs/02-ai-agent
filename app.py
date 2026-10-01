                #   AI AGENT WORKFLOW

# 1. User asks a question
#         ↓
# 2. AI model receives it
#         ↓
# 3. AI decides:
#    "I need to use Tool X"
#         ↓
# 4. AI sends a structured tool-call to Python
#         ↓
# 5. Python executes Tool X
#         ↓
# 6. Tool produces a result
#         ↓
# 7. Python sends the result back to the AI model
#         ↓
# 8. AI reads the result
#         ↓
# 9. AI gives the final answer to the user 
                    
# One important addition

# Steps 3–8 can happen multiple times.

# For example:

# User: "Find the cheapest laptop under ₹50,000 with 16 GB RAM and compare the top 3."

# The model might do:

# Model → Search laptops
# Python → Search
# Search → Results
# Python → Model

# Model → Search more details about Laptop A
# Python → Search
# Search → Results
# Python → Model

# Model → Search Laptop B
# Python → Search
# Search → Results
# Python → Model

# Model → "Now I have enough information."
#        ↓
# Final answer

# So an agent isn't necessarily:

# think → one tool → answer

# It can be:

# think → tool → observe → think → tool → observe → think → tool → observe → answer

# That repeated decision → action → result → decision loop is the key concept you were missing earlier.





                    # ┌──────────────────┐
                    # │      USER        │
                    # │ "Check EMP002's  │
                    # │  leave balance"  │
                    # └────────┬─────────┘
                    #          │
                    #          ▼
                    # ┌──────────────────┐
                    # │      QWEN3       │
                    # │                  │
                    # │ DECIDES:         │
                    # │ "Use the leave  │
                    # │  balance tool"   │
                    # └────────┬─────────┘
                    #          │
                    #    tool call
                    #          │
                    #          ▼
                    # ┌──────────────────┐
                    # │ check_leave_     │
                    # │ balance()        │
                    # └────────┬─────────┘
                    #          │
                    #          ▼
                    # "EMP002 has 18 days"
                    #          │
                    #          ▼
                    # ┌──────────────────┐
                    # │      QWEN3       │
                    # │                  │
                    # │ Creates final    │
                    # │ natural answer   │
                    # └────────┬─────────┘
                    #          │
                    #          ▼
                    # "EMP002 has 18 days
                    #  of leave remaining."

# app.py

# Import Ollama so Python can communicate with our local Qwen model.
# app.py

import ollama

# Import the actual Python functions that our agent can use.
from tools import (
    get_employee_info,
    check_leave_balance,
    create_it_ticket
)


# ---------------------------------------------------------
# 1. Describe the tools to Qwen
# ---------------------------------------------------------
# These descriptions tell Qwen:
#
# "These are the things you are allowed to ask Python to do."
#
# Qwen decides WHEN to use them.
# Python actually executes them.
# ---------------------------------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_info",
            "description": "Get an employee's name, department, and role.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID, such as EMP001 or EMP002."
                    }
                },
                "required": ["employee_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "check_leave_balance",
            "description": "Check how many leave days an employee has remaining.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID, such as EMP001 or EMP002."
                    }
                },
                "required": ["employee_id"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_it_ticket",
            "description": "Create an IT support ticket for an employee.",
            "parameters": {
                "type": "object",
                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID."
                    },
                    "issue": {
                        "type": "string",
                        "description": "The IT issue that needs to be reported."
                    }
                },
                "required": ["employee_id", "issue"]
            }
        }
    }
]


# ---------------------------------------------------------
# 2. Ask the user for a question
# ---------------------------------------------------------

question = input("\nWhat can I help you with? ")

# The conversation starts with the user's question.
messages = [
    {
        "role": "user",
        "content": question
    }
]


# ---------------------------------------------------------
# 3. Start the AGENT LOOP
# ---------------------------------------------------------
#
# This is the important part.
#
# Qwen can:
#
#   A. Request a tool
#   B. Receive the tool result
#   C. Request another tool
#   D. Finally answer the user
#
# Therefore we don't assume the agent needs exactly
# one tool call.
# ---------------------------------------------------------

while True:

    # Ask Qwen what it wants to do next.
    response = ollama.chat(
        model="qwen3:4b",
        messages=messages,
        tools=tools
    )

    # Get Qwen's message.
    assistant_message = response["message"]

    # ---------------------------------------------------------
# Show Qwen's thinking, if the model returned it.
# ---------------------------------------------------------
#
# Qwen3 can return a separate "thinking" field.
# This is useful while we are learning how an agent works.
#
# It might look something like:
#
# "The user wants both the department and leave balance.
#  I need to retrieve employee information and leave balance."
#
# The exact text depends on the model.
# ---------------------------------------------------------

    thinking = assistant_message.get("thinking", "")

    if thinking:
        print("\n--- Qwen Thinking ---")
        print(thinking)


# Add Qwen's response to the conversation history.
    messages.append(assistant_message)

    # Check whether Qwen requested any tools.
    tool_calls = assistant_message.get("tool_calls", [])

    # -----------------------------------------------------
    # If there are NO tool calls:
    #
    # Qwen has finished reasoning and produced its answer.
    # -----------------------------------------------------

    if not tool_calls:

        print("\n--- Final Answer ---")
        print(assistant_message.get("content", ""))

        break


    # -----------------------------------------------------
    # Qwen requested one or more tools.
    # -----------------------------------------------------

    for tool_call in tool_calls:

        # Extract the tool name Qwen selected.
        tool_name = tool_call["function"]["name"]

        # Extract the arguments Qwen generated.
        arguments = tool_call["function"]["arguments"]

        print("\n--- Tool Call ---")
        print("Tool:", tool_name)
        print("Arguments:", arguments)


        # -------------------------------------------------
        # Python executes the tool.
        # -------------------------------------------------

        if tool_name == "get_employee_info":

            tool_result = get_employee_info(
                arguments["employee_id"]
            )

        elif tool_name == "check_leave_balance":

            tool_result = check_leave_balance(
                arguments["employee_id"]
            )

        elif tool_name == "create_it_ticket":

            tool_result = create_it_ticket(
                arguments["employee_id"],
                arguments["issue"]
            )

        else:

            tool_result = "Unknown tool."


        print("Tool Result:", tool_result)


        # -------------------------------------------------
        # IMPORTANT:
        #
        # Send the result back to Qwen.
        #
        # Qwen now sees:
        #
        # "I asked Python to perform X,
        #  and Python returned Y."
        #
        # It can then decide what to do next.
        # -------------------------------------------------

        messages.append(
            {
                "role": "tool",
                "tool_name": tool_name,
                "content": str(tool_result)
            }
        )