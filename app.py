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
import ollama

# Import the actual Python functions that our agent is allowed to use.
from tools import (
    get_employee_info,
    check_leave_balance,
    create_it_ticket
)


# =========================================================
# 1. DEFINE THE TOOLS FOR THE LLM
# =========================================================
#
# We are telling Qwen:
#
# "These are the tools you have access to.
#  Decide yourself whether you need one."
#
# Notice that we are NOT telling Python:
#
#     if "leave" in question:
#
# Qwen makes that decision.
# =========================================================

tools = [

    {
        "type": "function",

        "function": {
            "name": "get_employee_info",

            "description": (
                "Get an employee's name, department, "
                "and job role using their employee ID."
            ),

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

            "description": (
                "Check how many days of leave an employee "
                "has remaining."
            ),

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

            "description": (
                "Create an IT support ticket when an employee "
                "has an IT-related problem such as a laptop issue."
            ),

            "parameters": {
                "type": "object",

                "properties": {
                    "employee_id": {
                        "type": "string",
                        "description": "The employee ID."
                    },

                    "issue": {
                        "type": "string",
                        "description": "Description of the IT problem."
                    }
                },

                "required": ["employee_id", "issue"]
            }
        }
    }
]


# =========================================================
# 2. GET THE USER'S QUESTION
# =========================================================

question = input("\nWhat can I help you with? ")


# =========================================================
# 3. SEND THE QUESTION + TOOLS TO QWEN
# =========================================================
#
# This is the important part.
#
# We are saying:
#
# "Here is the user's question.
# Here are the tools available to you.
# Decide what to do."
#
# Python does NOT choose the tool.
# =========================================================

messages = [
    {
        "role": "user",
        "content": question
    }
]


response = ollama.chat(
    model="qwen3:4b",

    messages=messages,

    tools=tools
)


# =========================================================
# 4. LOOK AT QWEN'S DECISION
# =========================================================

assistant_message = response["message"]


print("\n--- Qwen's Decision ---")
print(assistant_message)


# =========================================================
# 5. CHECK WHETHER QWEN REQUESTED A TOOL
# =========================================================

tool_calls = assistant_message.get("tool_calls", [])


if not tool_calls:

    # Qwen decided that no tool was necessary.

    print("\n--- Final Answer ---")

    print(assistant_message.get("content", ""))


else:

    # Qwen decided that one or more tools are necessary.

    print("\n--- Tool Call ---")

    for tool_call in tool_calls:

        # -------------------------------------------------
        # Get the name of the tool Qwen selected.
        # -------------------------------------------------

        tool_name = tool_call["function"]["name"]

        # -------------------------------------------------
        # Get the arguments Qwen selected.
        # -------------------------------------------------

        arguments = tool_call["function"]["arguments"]

        print("Tool:", tool_name)
        print("Arguments:", arguments)


        # =================================================
        # 6. PYTHON EXECUTES QWEN'S DECISION
        # =================================================
        #
        # This is NOT Python deciding which tool to use.
        #
        # Qwen already decided.
        #
        # Python's job here is simply:
        #
        # "Qwen asked me to execute this function,
        # so I will execute it."
        # =================================================

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


        print("\n--- Tool Result ---")
        print(tool_result)


        # =================================================
        # 7. GIVE THE TOOL RESULT BACK TO QWEN
        # =================================================
        #
        # This is extremely important.
        #
        # Qwen made a decision.
        #
        # The tool executed.
        #
        # Now Qwen gets to see what happened.
        # =================================================

        messages.append(assistant_message)

        messages.append(
            {
                "role": "tool",

                "content": str(tool_result)
            }
        )


    # =====================================================
    # 8. ASK QWEN FOR THE FINAL ANSWER
    # =====================================================

    final_response = ollama.chat(
        model="qwen3:4b",

        messages=messages,

        tools=tools
    )


    print("\n--- Final Answer ---")

    print(
        final_response["message"]["content"]
    )