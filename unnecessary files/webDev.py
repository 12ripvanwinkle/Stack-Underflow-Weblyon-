import os
from bs4 import BeautifulSoup
import threading
import time
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
# Function to start the server
def start_server():
    os.chdir("Portfolio_templates")  # Change directory to where the index.html is saved
    handler = SimpleHTTPRequestHandler
    with TCPServer(("", 8000), handler) as httpd:
        print("Server started at http://localhost:8000")
        httpd.serve_forever()

# Function to stop the server after input
def stop_server():
    input("Press Enter to stop the server...")
    print("Stopping the server...")
    print("Server stopped.") 

    # Graceful shutdown of the server (requires thread management for a clean exit)
    # In this example, stopping the server just terminates the process.
    os._exit(0)

def generator(template_path, user_data):
    from datetime import datetime
    # Load the template
    template = load_template(template_path)

    # # Generate project list
    # project_template = """
    #     <li>
    #         <h3>{name}</h3>
    #         <p>{description}</p>
    #     </li>
    # """
    # project_list = "".join(
    #     project_template.format(name=project["name"], description=project["description"])
    #     for project in user_data["projects"]
    # )

    # Add the address if it was provided
    # address_section = ""
    # if user_data["contact"].get("address"):  # Check if the address exists
    #     address_section = f'<li>Address: {user_data["contact"]["address"]}</li>'

    # Combine all data with the HTML template
    homepage = template.format(
        name = user_data["name"],
        occupation = user_data["occupation"],
        address = user_data["contact"]["address"],
        intro1 = user_data["intro1"],
        about_me_info = user_data["about_me_info"],
        phone = user_data["contact"]["phone"],
        email = user_data["contact"]["email"],
    )

    # Save the generated HTML to a file with UTF-8 encoding
    folder_path = "Portfolio_templates"
    # ensure the folder exists, otherwise create it
    os.makedirs(folder_path, exist_ok=True)
    # define the file path
    file_path = os.path.join(folder_path, 'index.html')
    # creates the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(homepage)
    print("HTML file generated successfully!")
    


def user_info_holder():
    user_info = {
        "name" : input('Enter your name: '),
        "occupation": input('Enter your occupation: '),
        "intro1": input('Enter something about your self: '),
        "about_me_info": input('Go into more detail: '),
        "contact": {
            "email": input("enter your email: "),
            "phone": input("Enter your phone number: "),
            "address": input("enter your parish/province/state: ")
        },
    }
    return user_info

def collect_user_info_portfolio(choice):
    if choice == "1":
        holder = user_info_holder()
    if choice == "2":
        holder = user_info_holder()
    return holder

def portfolio_type():
    print("choose between option 1 and option 2")
    choice = input("enter here: ")
    if choice == "1":
        user_info =  collect_user_info_portfolio(choice)
        generator("Portfolio_templates/template_1.html", user_info)
    elif choice == "2":
        user_info = collect_user_info_portfolio(choice)
        generator("Portfolio_templates/portfolio_template_0.html", user_info)

    pass

# Main Program
while True:
    print("Choose an option:")
    print("1: Generate a portfolio website")
    print("2: Generate an e-commerce website (Not implemented)")
    print("Enter 'exit' to close")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        portfolio_type()
        # Start the server in a separate thread
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

        # Wait for user input to stop the server
        stop_server()
        break
    elif choice == "exit":
        break
    else:
        print("Invalid choice. Please try again.")