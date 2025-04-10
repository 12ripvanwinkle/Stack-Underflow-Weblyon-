import os
import re
import shutil

def load_file(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None

def extract_editable_sections(html_content):
    """Extracts all editable sections from the HTML and returns them as a dict."""
    pattern = r"<!-- editable: (.*?) -->(.*?)<!-- endeditable -->"
    matches = re.findall(pattern, html_content, re.DOTALL)
    return {key.strip(): value.strip() for key, value in matches}

def update_editable_section(html_content, section_name, new_value):
    """Replaces the content of the given editable section with new_value."""
    pattern = rf"(<!-- editable: {re.escape(section_name)} -->)(.*?)(<!-- endeditable -->)"
    replacement = rf"\1{new_value}\3"
    return re.sub(pattern, replacement, html_content, flags=re.DOTALL)

def edit_html_file(file_path):
    html = load_file(file_path)
    if html is None:
        return

    while True:
        sections = extract_editable_sections(html)
        if not sections:
            print("❌ No editable sections found.")
            break

        print("\n🎯 Editable Sections Found:")
        for i, (key, val) in enumerate(sections.items(), 1):
            print(f"{i}. {key} → {val}")

        user_input = input("\nEnter the name of the section to edit (or type 'exit' to finish): ").strip()
        if user_input.lower() == "exit":
            break

        if user_input not in sections:
            print("❌ Invalid section name.")
            continue

        if user_input.lower() == "pfp":
            # Special handling for 'pfp' section (profile picture upload)
            new_picture_path = input("Enter the full path of the new profile picture: ").strip().strip('"').strip("'")
            new_picture_path = new_picture_path.replace("\\", "/")
            
            # Check if file exists
            if not os.path.exists(new_picture_path):
                print(f"❌ File not found: {new_picture_path}")
                print("⚠️ Skipping update due to image copy failure.")
                continue
            
            # Ensure 'images' folder exists next to the HTML file
            html_dir = os.path.dirname(file_path)
            images_dir = os.path.join(html_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            
            # Copy file into 'images' folder
            file_name_only = os.path.basename(new_picture_path)
            destination = os.path.join(images_dir, file_name_only)
            shutil.copy(new_picture_path, destination)

            # Update HTML to use relative path
            new_content = f'<img src="images/{file_name_only}" alt="Profile Picture">'
        else:
            new_content = input(f"Enter new content for '{user_input}': ").strip()

        html = update_editable_section(html, user_input, new_content)
        print("✅ Section updated.\n")

    # Save changes
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html)
    print("💾 All changes saved to the file.")

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
        edit_html_file(file_path)
    else:
        print("❌ Invalid choice. File not found.")

def copy_image_to_html_directory(image_path, html_file_path):
    """Copies the image to the same folder as the HTML file and returns just the new image name."""
    if not os.path.isfile(image_path):
        print(f"❌ File not found: {image_path}")
        return None

    html_dir = os.path.dirname(html_file_path)
    image_filename = os.path.basename(image_path)
    destination = os.path.join(html_dir, image_filename)

    try:
        shutil.copy(image_path, destination)
        print(f"📸 Image copied to {destination}")
        return image_filename
    except Exception as e:
        print(f"⚠️ Failed to copy image: {e}")
        return None

# Example usage
if __name__ == "__main__":
    folder1 = "User_Portfolio"
    folder2 = "User_Ecommerce"
    display_html_files(folder1, folder2)
