import os
import openai

import math
import pytz
from datetime import datetime
import inspect
import json
import datetime
import tiktoken
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")




# Globale Variablen
result = ''
chat_user = []
context =""


def calculator(num1, num2, operator):
    if operator == '+':
        return str(num1 + num2)
    elif operator == '-':
        return str(num1 - num2)
    elif operator == '*':
        return str(num1 * num2)
    elif operator == '/':
        return str(num1 / num2)
    elif operator == '**':
        return str(num1 ** num2)
    elif operator == 'sqrt':
        return str(math.sqrt(num1))
    else:
        return "Invalid operator"

def get_current_time(location):
    try:
        # Get the timezone for the city
        timezone = pytz.timezone(location)

        # Get the current time in the timezone
        now = datetime.now(timezone)
        current_time = now.strftime("%I:%M:%S %p")

        return current_time
    except:
        return "Sorry, I couldn't find the timezone for that location."

def check_args(function, args):
    sig = inspect.signature(function)
    params = sig.parameters

    # Check if there are extra arguments
    for name in args:
        if name not in params:
            return False
    # Check if the required arguments are provided
    for name, param in params.items():
        if param.default is param.empty and name not in args:
            return False

    return True

functions = [
        {
            "name": "get_current_time",
            "description": "Die aktuelle Zeit zu erhalten an einem gewissen Ort",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location name. The pytz is used to get the timezone for that location. Location names should be in a format like America/New_York, Asia/Bangkok, Europe/London",
                    }
                },
                "required": ["location"],
            },
        },
        {
            "name": "calculator",
            "description": "Ein simpler Taschenrechner um simple arithmetische operationen auszuführen",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number"},
                    "num2": {"type": "number"},
                    "operator": {"type": "string", "enum": ["+", "-", "*", "/", "**", "sqrt"]},
                },
                "required": ["num1", "num2", "operator"],
            },
        },
]

available_functions = {
    "get_current_time": get_current_time,
    "calculator": calculator,
}

def first_think_llm(user, functions, available_functions):
    history = '\n'.join([f"{message['role']}: {message['content']}" for message in chat_user])

    messages = [
        {"role": "system",
         "content":
             "You are a Customer Supporter for the Zurich Insurance and your Name ist ZüriZap."
             "Your job is to answer questions about your client's insurance policies."
             "YOU SHOULD USE THE INFORMATION BELOW TO ANSER THE QUESTION FROM THE USER:"
             f"{context}"
             f"HERE YOU FIND THE HISTORY FROM THE CHAT"
             f"{history}"
             },
        {"role": "user", "content":
            f""
            f"First you have to decide whether you may answer the following question of the: {user}. "
            f"You may only answer questions on the topic Insurance Policies and Zurich Insurance"
         }
    ]

    # Erstellt eine Text Completion mit OpenAI
    response = openai.ChatCompletion.create(
        engine="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature = 0.5,
        max_tokens = 8000,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0,
        stop = None,

    )
    chat_message = response['choices'][0]['message']['content']

    return chat_message



def chatbot():

    user = input("Bot: Hey I'm ZüriZap how can I help you??\nUser: ")
    chat_user.append({"role": "assistant", "content": "Hey I'm ZüriZap how can I help you?" })

    while True:
        chat_user.append({"role": "user", "content": user})
        print("Bot: " + first_think_llm(user,functions,available_functions) )
        user = input("\nUser:")


# Durchführung der Funktionen
chatbot()