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

def ai_helper(occupation, section):
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

def business_info_getter(business_type):
    name = input("Enter the name of your business: ")
    ai_ans = input("Do you want to use AI to generate your portfolio? (y/n): ").lower()
    if ai_ans == "y":
        print("The AI is generating text for you")
        intro1 = ai_helper("Cafe", "1")
        print("The AI is generating more text for you")
        about_me_info = ai_helper("Cafe", "2")
    else:
        intro1 = input("Enter a 15 word short intro about your business: ")
        about_me_info = input("Enter a 40 word extract going into detail about why you should choose your business: ")

    history = input("Enter a brief history of your business: ")
    email = input("Enter the business' email: ")
    phone = input("Enter the business' phone number: ")
    address = input("Enter the business' address: ")
    reviews = []
    for i in range(3):  
        review = input(f"Enter review {i + 1} of your business: ")
        reviews.append(review)
    products = []
    num_products = int(input("Enter the number of products you want to add: "))
    for i in range(num_products):
        product = input(f"Enter product {i + 1}: ")
        products.append(product)
    product_images = []
    print("Enter", num_products, " file path to images for your products")
    for i in range (num_products):
        image = input("Enter the path to your profile picture: ").strip('"')
        product_images.append(image)
    pfp = input("Enter the path to your profile picture: ").strip('"')

    ecommerce_info = {
        "name": name,
        "intro1": intro1,
        "about_me_info": about_me_info,
        "history": history,
        "contact": {
            "email": email,
            "phone": phone,
            "address": address
        },
        "reviews": reviews,
        "products": products,
        "images": product_images,
        "pfp": pfp
    }

    return ecommerce_info

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def ecommerce_type():
    print("Enter the portfolio of your choosing by entering the corresponding number")
    choice = input("1.Cafe Website\n2.Gym Website\n")
    match choice:
        case "1":
            print("Cafe Website")
            info = business_info_getter("Cafe")
            template = load_template("Ecommerce_templates\Cafeindex.html")
            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\Cafestyle.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Ecommerce"
            # Copy the file
            shutil.copy(source_path, destination_folder)

            # Define the source and destination paths
            source_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Ecommerce_templates\cafe_images"
            destination_images_folder = os.path.join(destination_folder, "cafe_images")  # Ensure correct destination

            # Copy the entire 'cafe_images' folder
            shutil.copytree(source_folder, destination_images_folder)

            generator(info, template)
        case "2":
            print("Gym Website")

        case _:
            print("Invalid choice")
            return ecommerce_type()
        
def generator(info,template):
    # Move the image to the project folder
    destination_folder = "User_Ecommerce"
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the image to the destination folder
    destination_path = os.path.join(destination_folder, os.path.basename(info["pfp"]))
    shutil.copy(info["pfp"], destination_path)

    # Set the relative path for the HTML
    pfp_path = f"{os.path.basename(info['pfp'])}"

     # Generate dynamic product boxes
    product_boxes = ""
    for product in info["products"]:
            product_boxes += f'''
                <div class="box">
                    <img src="cafe_images/american.jpg" alt="">
                    <h3>{product}</h3>
                    <div class="content">
                        <span>$25</span>
                        <a href="#">Add to cart</a>
                    </div>
                </div>
            '''
        # Update the template with dynamic products
    
    page = template.format(name=info["name"],
            intro1=info["intro1"],
            about_me_info=info["about_me_info"],
            history=info["history"],
            address=info["contact"]["address"],
            phone=info["contact"]["phone"],
            email=info["contact"]["email"],
            review1=info["reviews"][0],
            review2=info["reviews"][1],
            review3=info["reviews"][2],
            pfp=pfp_path,
            products=product_boxes
    )
    # Save the generated HTML to a file with UTF-8 encoding
    folder_path = destination_folder
    # ensure the folder exists, otherwise create it
    os.makedirs(folder_path, exist_ok=True)
    # define the file path
    file_name = input("Enter the name of the file (do not enter '.html'): ")
    file_path = os.path.join(folder_path, file_name + ".html")
    # creates the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page)

    # Open the HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(file_path)}")

    # # Copy the image to the destination folder
    # destination_path = os.path.join(destination_folder, os.path.basename(info["pfp"]))
    # shutil.copy(info["pfp"], destination_path)
    
    # # Retrieve image list from the dictionary
    # images = info.get("images", [])

    # # Copy each image to the destination folder
    # for image in images:
    #     if os.path.exists(image):
    #         destination_path = os.path.join(destination_folder, os.path.basename(image))
    #         shutil.copy(image, destination_path)
    #         print(f"Copied {image} to {destination_path}")
    #     else:
    #         print(f"Error: {image} not found!")

    # print("Image copying process completed.")
    

if __name__ == "__main__":
    ecommerce_type()