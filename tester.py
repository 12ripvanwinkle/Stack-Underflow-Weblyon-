from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
from bs4 import BeautifulSoup
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from datetime import datetime

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
# chains them together using langchain
chain = prompt | model

def start_server(template_type):
    if template_type == "Portfolio":
        directory = "Portfolio_templates"
    elif template_type == "Ecommerce":
        directory = "Ecommerce_templates"

    os.chdir(directory)  # Change directory to where the index.html is saved

    class CustomHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.path = "/index.html"  # Redirect root requests to index.html
            return super().do_GET()

    with TCPServer(("", 8000), CustomHandler) as httpd:
        print(f"Server started at http://localhost:8000")
        httpd.serve_forever()

# Start the server in a separate thread
def start_server_thread(template_type):
    server_thread = threading.Thread(target=start_server, args=(template_type,), daemon=True)
    server_thread.start()
    print(f"Server thread started for {template_type}!")
        
# Function to stop the server after input
def stop_server():
    input("Press Enter to stop the server...")
    print("Stopping the server...")
    print("Server stopped.") 

    # Graceful shutdown of the server (requires thread management for a clean exit)
    # In this example, stopping the server just terminates the process.
    os._exit(0)

def helper_test(occupation, section, wtype):
    context = ""
    if wtype == "Portfolio":
        if section == "1":
            user_input = f"write a 15 word short intro about me as a {occupation} without including names or anything such as [your name] no need to type anything like 'Here's a 40-word extract:"
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot: ", result)
            context += f"\nUser: {user_input}\nAI: {result}"
            return satisfaction(context, result)

        if section == "2":
            user_input = f"ok can you give me a 40 word extract going into detail about me being a {occupation} no need to type anything like 'Here's a 40-word extract:'"
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot: ", result)
            context += f"\nUser: {user_input}\nAI: {result}"
            return satisfaction(context, result)
    elif wtype == "Ecommerce":
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
        

def satisfaction(context,result):
    ans = input("are you satisfied with this response if yes enter 'yes' else 'no': ")
    if ans.lower() == "no":
        while 1:
            user_input = "Give me a better 1 just the text alone no need to type anything like 'Here's a 40-word extract:' or 'Here's a 15-word extract:'"
            result = chain.invoke({"context": context, "question": user_input})
            print("Bot: ", result)
            ans_again = input("If satisfied enter 1 else 2: ")
            if ans_again == "1":
                break
            else:
                continue
    elif ans.lower() != "Yes" or ans == "Yes":
        print("I take it you meant yes")
    return result


def user_info_holder(ptype):
    if ptype == "1":
        name = input('Enter your name: ')
        occupation = input('Enter your occupation: ')
        ans = input("Would you like our ai to help you fill out some fields for you enter 'yes' or 'no': ")
        if ans == "yes":
            print("The ai is generating text for you")
            intro1 = helper_test(occupation, "1", "Portfolio")
            print("The ai is generating somemore text for you")
            about_me_info = helper_test(occupation, "2", "Portfolio")
        else:
            intro1 = input('Enter something about yourself: ')
            about_me_info = input('Go into more detail: ')
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        address = input("Enter your parish/province/state: ")

        user_info = {
            "name": name,
            "occupation": occupation,
            "intro1": intro1,
            "about_me_info": about_me_info,
            "contact": {
                "email": email,
                "phone": phone,
                "address": address
            },
        }

    elif ptype == "2":
        name = input('Enter your name: ')
        occupation = input('Enter your occupation: ')
        ans = input("Would you like our ai to help you fill out some fields for you enter 'yes' or 'no': ")
        if ans == "yes":
            print("The ai is generating text for you")
            intro1 = helper_test(occupation, "1", "Portfolio")
            print("The ai is generating somemore text for you")
            about_me_info = helper_test(occupation, "2", "Portfolio")
        else:
            intro1 = input('Enter something about yourself: ')
            about_me_info = input('Go into more detail: ')
            email = ""
            phone = ""
            address = ""
        
        user_info = {
            "name": name,
            "occupation": occupation,
            "intro1": intro1,
            "about_me_info": about_me_info,
            "contact": {
                "email": email,
                "phone": phone,
                "address": address
            },
        }
    
    return user_info

def ecommerce_info_holder(bus_type):
    name = input('Enter the name of your business: ')
    ans = input("Would you like our ai to help you fill out some fields for you enter 'yes' or 'no': ")
    if ans == "yes":
        print("The ai is generating text for you")
        intro1 = helper_test(bus_type, "1", "Portfolio")
        print("The ai is generating somemore text for you")
        about_me_info = helper_test(bus_type, "2", "Portfolio")
    else:
        intro1 = input('Enter a short description of your business: ')
        about_me_info = input('Go into more detail as to why people should choose your business: ')

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
        "products": products
    }
    return ecommerce_info

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generator(info, template, wtype):
    
    if wtype == "Portfolio":
        page = template.format(
            name = info["name"],
            
            occupation = info["occupation"],
            address = info["contact"]["address"],
            intro1 = info["intro1"],
            about_me_info = info["about_me_info"],
            phone = info["contact"]["phone"],
            email = info["contact"]["email"],
        )
        # Save the generated HTML to a file with UTF-8 encoding
        folder_path = "Portfolio_templates"
        # ensure the folder exists, otherwise create it
        os.makedirs(folder_path, exist_ok=True)
        # define the file path
        file_path = os.path.join(folder_path, 'index.html')
        # creates the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(page)

    if wtype == "Ecommerce":
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
        page = template.format(
            name=info["name"],
            intro1=info["intro1"],
            about_me_info=info["about_me_info"],
            history=info["history"],
            address=info["contact"]["address"],
            phone=info["contact"]["phone"],
            email=info["contact"]["email"],
            review1=info["reviews"][0],
            review2=info["reviews"][1],
            review3=info["reviews"][2],
            products=product_boxes  # Insert the dynamically generated product list
        )

        folder_path = "Ecommerce_templates"
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, "index.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page)

    print("HTML file generated successfully!")


def portfolio_type():
    ans = input("Choose between option 1 and 2: ")
    if ans == "1":
        portfolio_template = load_template("Portfolio_templates/portfolio_template_0.html")
        user_info = user_info_holder("1")
        generator(user_info, portfolio_template, "Portfolio")
        start_server_thread("Portfolio")
        # Wait for user input to stop the server
        stop_server()
        
    if ans == "2":
        portfolio_template = load_template("Portfolio_templates/portfolio_template_1.html")
        user_info = user_info_holder("2")
        generator(user_info, portfolio_template, "Portfolio")
        start_server_thread("Portfolio")
        # Wait for user input to stop the server
        stop_server()

def Ecommerce_type():
    choice = input("Choose between option 1 and 2: ")
    if choice == "1":
        ecommerce_template = load_template("Ecommerce_templates/Cafeindex.html")
        ecommerce_info = ecommerce_info_holder("Cafe")
        generator(ecommerce_info, ecommerce_template, "Ecommerce")
        start_server_thread("Ecommerce")

        # Wait for user input to stop the server
        stop_server()
        pass
    if choice == "2":
        pass

import requests
def submitter(holder):
    url = "http://127.0.0.1:5000/chat"
    headers = {"Content-Type": "application/json"}
    data = {"Text": "Hello, this is a test message", "ProjectID":1}


    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:  # 201 means resource created
        print("Successfully submitted:", response.json())
    else:
        print("Error:", response.status_code, response.text)
    pass

def upload_project_file(project_file, project_id,file_type):
        # Define the URL where the file will be uploaded
    url = 'http://127.0.0.1:5000/projects/1/upload/js'

    # Define the file path
    # file_path = '/Users/carlyon/Documents/Projects/Assignment/Capstone/Stack-Underflow-Project/Portfolio_templates/portfolio_template_script1.js'

    # Open the file in binary mode and prepare the payload
    files = {'file': open(project_file, 'rb')}
    data = {'project_id': project_id, 'file_type': file_type}

    # Send the POST request
    response = requests.post(url, files=files)

    # Close the file after uploading
    files['file'].close()

    # Check the response from the server
    if response.status_code == 200:
        print("File uploaded successfully:", response.json())
    else:
        print("Failed to upload file. Status code:", response.status_code, response.text)
    
    pass
if __name__ == "__main__":

    upload_project_file("unnecessary files/jsonTester.js", 1, "js")
    