import http.server
import socketserver
import os
import json
import requests
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Constants
PORT = 8000
TEMPLATE_FOLDER = "website"

class AIHelper:
    """Handles AI-generated content using LangChain and Ollama."""
    
    def __init__(self, model="mistral"):
        self.llm = Ollama(model=model)
    
    def generate_text(self, prompt):
        """Generates AI text based on the given prompt."""
        return self.llm.invoke(prompt)

class WebServer:
    """Handles the local web server for previewing websites."""
    
    def __init__(self, port=PORT):
        self.port = port
        self.handler = http.server.SimpleHTTPRequestHandler
    
    def start(self):
        """Starts the HTTP server."""
        with socketserver.TCPServer(("", self.port), self.handler) as httpd:
            print(f"Serving at http://localhost:{self.port}")
            httpd.serve_forever()
    
    def stop(self):
        """Stops the HTTP server."""
        print("Stopping server...")
        os._exit(0)

class UserInfo:
    """Stores user details for portfolio or e-commerce sites."""
    
    def __init__(self, user_type):
        self.user_type = user_type
        self.data = {}
    
    def collect_info(self):
        """Collects user input based on the selected website type."""
        if self.user_type == "Portfolio":
            self.data["name"] = input("Enter your name: ")
            self.data["bio"] = input("Enter a short bio: ")
            self.data["projects"] = input("Enter your projects (comma-separated): ").split(",")
        elif self.user_type == "Ecommerce":
            self.data["business_name"] = input("Enter your business name: ")
            self.data["description"] = input("Enter a short business description: ")
            self.data["products"] = input("Enter your products (comma-separated): ").split(",")
        else:
            raise ValueError("Invalid website type selected!")
    
    def get_info(self):
        """Returns collected user information."""
        return self.data

class TemplateGenerator:
    """Handles loading and modifying HTML templates."""
    
    def __init__(self, template_folder=TEMPLATE_FOLDER):
        self.template_folder = template_folder
    
    def generate_html(self, user_info):
        """Creates an HTML file with user data."""
        file_path = os.path.join(self.template_folder, "index.html")
        with open(file_path, "w") as f:
            if "name" in user_info:
                # Portfolio template
                content = f"<h1>{user_info['name']}</h1><p>{user_info['bio']}</p>"
            else:
                # E-commerce template
                content = f"<h1>{user_info['business_name']}</h1><p>{user_info['description']}</p>"
            
            f.write(content)
            print("Generated HTML file successfully!")

class ProjectUploader:
    """Handles uploading project data to a remote API."""
    
    def __init__(self, api_url):
        self.api_url = api_url
    
    def upload_data(self, data):
        """Uploads JSON data to the API."""
        response = requests.post(self.api_url, json=data)
        if response.status_code == 200:
            print("Data uploaded successfully!")
        else:
            print(f"Upload failed: {response.status_code}")

class WebsiteBuilder:
    """Main class to integrate all functionalities."""
    
    def __init__(self):
        self.ai_helper = AIHelper()
        self.template_gen = TemplateGenerator()
    
    def run(self):
        """Main execution flow."""
        site_type = input("Choose website type (Portfolio/Ecommerce): ")
        user_info = UserInfo(site_type)
        user_info.collect_info()

        # Generate AI-assisted text (optional)
        ai_text = self.ai_helper.generate_text("Generate a short description for a website.")
        print("AI-generated text:", ai_text)
        
        # Generate HTML
        self.template_gen.generate_html(user_info.get_info())

        # Start the local web server
        server = WebServer()
        server.start()

# Run the application
if __name__ == "__main__":
    app = WebsiteBuilder()
    app.run()
