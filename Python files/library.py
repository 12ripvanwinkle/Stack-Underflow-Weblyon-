import os
import webbrowser
import shutil

def load_file(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def display_html_files(folder1, folder2):

    folders = [folder1, folder2]
    html_files = {}

    print("🔍 Scanning for HTML files...\n")

    for folder in folders:
        print(f"📁 Reading from folder: {folder}")
        try:
            for file_name in os.listdir(folder):
                if file_name.endswith(".html"):
                    name_only = file_name[:-5]  # remove '.html'
                    file_path = os.path.join(folder, file_name)
                    print(f"  ➜ Found: {file_name}")
                    html_files[name_only] = file_path
        except FileNotFoundError:
            print(f"❌ Error: Folder '{folder}' not found!")
        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

    if not html_files:
        print("\n🚫 No HTML files found.")
        return
    
    choice = input("Which File Do you wish to edit (enter the file name): ").strip()

    if choice in html_files:
        file_path = html_files[choice]
        file_content = load_file(file_path)
        if file_content:
            print("\n✅ File loaded successfully!\n")
        else:
            print("❌ Could not read the file.")
    else:
        print("❌ Invalid choice. File not found.")


if __name__ == "__main__":
    # Example usage of the function
    folder1 = "User_Portfolio"
    folder2 = "User_Ecommerce"
    display_html_files(folder1, folder2)