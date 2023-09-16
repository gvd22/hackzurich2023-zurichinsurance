import inspect

import openai
import json
import os
# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_KEY")
user_chat_history = []



def get_current_status_of_claim(information):
    """Get the current weather in a given location"""
    status_info = {
        "status": "pending",
    }
    return json.dumps(status_info)

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
        "name": "get_current_status_of_claim",
        "description": "Get the current Status for the claim from the user",
        "parameters": {
            "type": "object",
            "properties": {
                "information": {
                    "type": "string",
                },
            },
            "required": ["information"],
        },
    },
    {
        "name": "get_current_status_of_test",
        "description": "",
        "parameters": {
            "type": "object",
            "properties": {
                "information": {
                    "type": "string",
                },
            },
            "required": ["information"],
        },
    }
]

available_functions = {
            "get_current_status_of_claim": get_current_status_of_claim,
        }


def run_conversation(user_input,functions,available_functions):
    # Step 1: send the conversation and available functions to GPT
    messages = [
        {"role": "system",
         "content":
             "You are a Customer Supporter for the Zurich Insurance and your Name ist ZüriZap."
             "Your job is to answer questions about your client's insurance policies."
         },
        {"role": "user", "content": user_input }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
          # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]

        if function_name not in available_functions:
            return "Function " + function_name + " does not exist"
        function_to_call = available_functions[function_name]

        # verify function has correct number of arguments
        function_args = json.loads(response_message["function_call"]["arguments"])
        if check_args(function_to_call, function_args) is False:
            return "Invalid number of arguments for function: " + function_name
        function_response = function_to_call(**function_args)

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response

        response = second_response['choices'][0]['message']['content']
        return response
    else:
        chat_message = response['choices'][0]['message']['content']
        return chat_message





#print(run_conversation(functions,available_functions))

def chatbot():

    print("Bot: Hey I'm ZüriZap how can I help you?")
    user_input = input("User: ")
    user_chat_history.append({"role": "assistant", "content": "Hey I'm ZüriZap how can I help you?" })

    while True:
        user_chat_history.append({"role": "user", "content": user_input})
        print("Bot: ", end="")
        print(run_conversation(user_input,functions,available_functions))
        user_input = input("User:")


chatbot()
