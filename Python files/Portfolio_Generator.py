# code for portfolio generators exclusively
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
    if section == 1:
        user_input = f"write a 15 word short intro about me as a {occupation} without including names or anything such as [your name] no need to type anything like 'Here's a 40-word extract:"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)
    if section == 2:
        user_input = f"ok can you give me a 40 word extract going into detail about me being a {occupation} no need to type anything like 'Here's a 40-word extract:'"
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
        return satisfaction(context, result)

def user_info_getter():
    name = input("Enter your name: ")
    occupation = input("Enter your occupation: ")
    ai_ans = input("Do you want to use AI to generate your portfolio? (y/n): ").lower()
    
    if ai_ans == "y":

        print("The ai is generating text for you")
        intro1 = ai_helper(occupation, 1, "Portfolio")
        print("The ai is generating somemore text for you")
        about_me_info = ai_helper(occupation, 2, "Portfolio")
    else:
        intro1 = input("Enter a 15 word short intro about you for the hero section: \n")
        about_me_info = input("Enter a 40 word extract about you for the about me section: \n")
    pfp = input("Enter the path to your profile picture: ").strip('"')
    user_info = {
            "name": name,
            "occupation": occupation,
            "intro1": intro1,
            "about_me_info": about_me_info,
            "pfp":pfp
        }
    return user_info

def contact_info_getter():
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    address = input("Entere your Parish/State/Province: ")

    contact_info = {
        "email": email,
        "phone": phone,
        "address": address
    }
    return contact_info

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
        
def portfolio_type():
    print("Enter the portfolio of your choosing by entering the corresponding number")
    choice = input("0. Portfolio 0\n1. Portfolio 1\n2. Portfolio 2\n")
    match choice:
        case "0":
            print("Portfolio 1")
            user_info = user_info_getter()
            contact_info = contact_info_getter()

            # Update in place
            user_info.update(contact_info)
            template = load_template("Portfolio_templates/portfolio_template_0.html")
            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_style0.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio"
            # Copy the file
            shutil.copy(source_path, destination_folder)

            generator(user_info, template, False)
        case "1":
            print("Portfolio 2")
            user_info = user_info_getter()
            template = load_template("Portfolio_templates/portfolio_template_1.html")

            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_style1.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio"
            # Copy the file
            shutil.copy(source_path, destination_folder)

            generator(user_info, template, True)
        case "2":
            print("Portfolio 3")
        case _:
            print("Invalid choice")
            portfolio_type()

def update_skills(html_file, services):
    # Read the existing HTML file
    with open(html_file, "r", encoding="utf-8") as file:
            content = file.read()
    if services == False:
        # Extract the current skills list using regex
        skills_pattern = re.search(r'(<div class="skills">\s*<ul>)(.*?)(</ul>\s*</div>)', content, re.DOTALL)
        
        if not skills_pattern:
            print("Skills section not found in the file.")
            return
        
        # Prompt the user for new skills
        new_skills = input("Enter skills separated by commas: ").split(",")

        # Trim whitespace and remove empty entries
        new_skills = [skill.strip() for skill in new_skills if skill.strip()]

        # Generate new <li> elements for the skills
        new_skills_html = "\n".join([f'                    <li><span><i class="bx bx-chevron-right"></i> {skill}</span></li>' for skill in new_skills])

        # Replace the existing skills with the new list
        updated_content = re.sub(r'(<div class="skills">\s*<ul>)(.*?)(</ul>\s*</div>)',
                                rf'\1\n{new_skills_html}\n                \3', content, flags=re.DOTALL)
    else:
        # Extract the current services section using regex
        services_pattern = re.search(r'(<div class="services-container">)(.*?)(</div>\s*</section>)', content, re.DOTALL)

        if not services_pattern:
            print("Services section not found in the file.")
            return

        # Prompt the user for new services
        services_input = input("Enter services separated by commas (name: description): ").split(",")

        # Trim whitespace and remove empty entries
        services = [service.strip() for service in services_input if service.strip()]

        # Generate new service HTML
        new_services_html = "\n".join([f'''
            <div class="service-box">
                <div class="service-info">
                    <h4>{service.split(':')[0].strip()}</h4>
                    <p>{service.split(':')[1].strip()}</p>
                </div>
            </div>''' for service in services])

        # Replace the existing services section with the new one
        updated_content = re.sub(r'(<div class="services-container">)(.*?)(</div>\s*</section>)',
                                rf'\1\n{new_services_html}\n        \3', content, flags=re.DOTALL)

    # Write the updated HTML back to the file
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("Skills updated successfully!")

def generator(info, template, wtype):
    # Move the image to the project folder
    destination_folder = "User_Portfolio"
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the image to the destination folder
    destination_path = os.path.join(destination_folder, os.path.basename(info["pfp"]))
    shutil.copy(info["pfp"], destination_path)
      
    # Set the relative path for the HTML
    pfp_path = f"{os.path.basename(info['pfp'])}"
    # Use .get() to avoid KeyError if key doesn't exist
    if not info.get("phone") and not info.get("email") and not info.get("address"):
        page = template.format(
            name = info["name"],
            
            occupation = info["occupation"],
            intro1 = info["intro1"],
            about_me_info = info["about_me_info"],
            pfp = pfp_path,            
            phone=info.get("phone", ""),  # Default to empty string if 'phone' doesn't exist
            email=info.get("email", ""),
            address=info.get("address", "")
        )
    else:
        page = template.format(
                name = info["name"],
                occupation = info["occupation"],
                address = info["address"],
                intro1 = info["intro1"],
                about_me_info = info["about_me_info"],
                phone = info["phone"],
                email = info["email"],
                pfp = pfp_path
            )

    # Save the generated HTML to a file with UTF-8 encoding
    folder_path = "User_Portfolio"
    # ensure the folder exists, otherwise create it
    os.makedirs(folder_path, exist_ok=True)
    # define the file path
    file_name = input("Enter the name of the file (do not enter '.html'): ")
    file_path = os.path.join(folder_path, file_name + ".html")
    # creates the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(page)

    update_skills("User_Portfolio" + "\\" + file_name + ".html", wtype)

    # upload_project_file("C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio", 1, "js")

    # Open the HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(file_path)}")

# def submitter(holder):
#     url = "http://127.0.0.1:5000/chat"
#     headers = {"Content-Type": "application/json"}
#     data = {"Text": "Hello, this is a test message", "ProjectID":1}


#     response = requests.post(url, json=data, headers=headers)

#     if response.status_code == 201:  # 201 means resource created
#         print("Successfully submitted:", response.json())
#     else:
#         print("Error:", response.status_code, response.text)
#     pass

# def upload_project_file(project_file, project_id,file_type):
#         # Define the URL where the file will be uploaded
#     url = 'http://127.0.0.1:5000/projects/1/upload/js'

#     # Define the file path
#     # file_path = '/Users/carlyon/Documents/Projects/Assignment/Capstone/Stack-Underflow-Project/Portfolio_templates/portfolio_template_script1.js'

#     # Open the file in binary mode and prepare the payload
#     files = {'file': open(project_file, 'rb')}
#     data = {'project_id': project_id, 'file_type': file_type}

#     # Send the POST request
#     response = requests.post(url, files=files)

#     # Close the file after uploading
#     files['file'].close()

#     # Check the response from the server
#     if response.status_code == 200:
#         print("File uploaded successfully:", response.json())
#     else:
#         print("Failed to upload file. Status code:", response.status_code, response.text)
#     pass

if __name__ == "__main__":
    # upload_project_file("C:\\Users\\nites\\OneDrive\\Desktop\\Stack-Underflow-Weblyon-\\User_Portfolio\\jsonTester.js", 1, "js")
    portfolio_type()
