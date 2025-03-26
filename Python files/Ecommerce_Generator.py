# code for Ecommerce generators exclusively
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
from bs4 import BeautifulSoup
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from datetime import datetime
import requests
from PIL import Image
import shutil
import webbrowser
import re

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
# chains them together using langchain
chain = prompt | model

def satisfaction(context, result):
    ans = input("are you satisfied with this response if yes enter 'yes' else 'no': ")
    if ans.lower() == "no":
        while 1:
            user_input = "Give me a better answer just the text alone no need to type anything like 'Here's a 40-word extract:' or 'Here's a 15-word extract:'"
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot: ", result)
            ans_again = input("If satisfied enter 1 else 2: ")
            if ans_again == "1":
                break
            else:
                continue
    elif ans.lower() != "Yes" or ans == "Yes":
        print("Great!")
    return result

def ai_helper(occupation, section, web_type):
    context=""
    if section == "1":
        user_input = f"write a 15 word short intro about my business which is a {occupation} without including names or anything such as [your name] no need to type anything like 'Here's a 40-word extract:"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)
    if section == "2":
        user_input = f"ok can you give me a 40 word extract going into detail about why you should choose my business which is a {occupation} no need to type anything like 'Here's a 40-word extract:'"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)

def business_info_getter():
    name = input("Enter the name of your business: ")
    ai_ans = input("Do you want to use AI to generate your portfolio? (y/n): ")
    pass

def ecommerce_type():
    print("Enter the portfolio of your choosing by entering the corresponding number")
    choice = input("1.Cafe Website\n2.Gym Website\n")
    match choice:
        case "1":
            print("Cafe Website")
            
        case "2":
            print("Gym Website")

        case _:
            print("Invalid choice")
            return ecommerce_type()

if __name__ == "__main__":
    ecommerce_type()