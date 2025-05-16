# portfolio_generator.py
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3")
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def generate_intro_and_about_me(occupation):
    context = ""
    intro_prompt = f"write a 15 word short intro about me as a {occupation}..."
    about_me_prompt = f"ok can you give me a 40 word extract going into detail about me being a {occupation}..."

    intro = chain.invoke({"context": context, "question": intro_prompt})
    context += f"\nUser: {intro_prompt}\nAI: {intro}"

    about = chain.invoke({"context": context, "question": about_me_prompt})
    return intro, about
