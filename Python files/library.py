import os
import webbrowser
import shutil

def display_html_files(folder1, folder2):

    # List of HTML files to ignore
    ignore_files = ["portfolio_template_1.html", "portfolio_template_0.html", "Cafeindex.html"]

    # Combine the two folders into a list
    folders = [folder1, folder2]
    
    for folder in folders:
        print(f"\n📁 Reading from folder: {folder}")
        
        try:
            # List all files in the current folder
            for file_name in os.listdir(folder):
                if file_name.endswith(".html") and file_name not in ignore_files:
                    file_path = os.path.join(folder, file_name)
                    print(f"Found HTML file: {file_name}")
                    
                    # Open the HTML file in the default browser
                    # webbrowser.open(f"file://{os.path.abspath(file_path)}")
        
        except FileNotFoundError:
            print(f"Error: Folder '{folder}' not found!")
        except Exception as e:
            print(f"An error occurred: {e}")

# Example usage
folder_path_1 = "Portfolio_templates"
folder_path_2 = "Ecommerce_templates"
display_html_files(folder_path_1,folder_path_2)
