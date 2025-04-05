import re

html_file = "User_Portfolio/tester3.html"  # Change to your actual HTML filename

# Read the HTML content
with open(html_file, "r", encoding="utf-8") as file:
    content = file.read()

# Match the full service block including icons
pattern = re.search(
    r'(<div class="services-container">\s*<div class="grid">)(.*?)(</div>\s*</div>)',
    content,
    re.DOTALL
)

if not pattern:
    print("Services section not found.")
    exit()

# Extract the icon classes in order
icon_classes = re.findall(r'<i class="fa-solid ([^"]+)"></i>', pattern.group(2))

if not icon_classes:
    print("No icon classes found.")
    exit()

# Prompt the user for new content (excluding icons)
print("Enter service details in this format: Title, Years, Description")
print("One per line. Enter exactly", len(icon_classes), "lines.")

services = []
for i in range(len(icon_classes)):
    user_input = input(f"Service #{i+1}: ").strip()
    try:
        title, years, desc = [item.strip() for item in user_input.split(",")]
    except ValueError:
        print("⚠️ Invalid format. Use: Title, Years, Description")
        exit()
    services.append((title, years, desc))

# Generate new HTML blocks with preserved icons
service_blocks = []
for i, (title, years, desc) in enumerate(services):
    icon = icon_classes[i]
    block = f'''
        <div class="grid-card">
            <i class="fa-solid {icon}"></i>
            <span>{title}</span>
            <h3>{years}</h3>
            <p>{desc}</p>
        </div>'''
    service_blocks.append(block)

# Join all new blocks
new_services_html = "\n".join(service_blocks)

# Replace old HTML block with new one
updated_content = re.sub(
    r'(<div class="services-container">\s*<div class="grid">)(.*?)(</div>\s*</div>)',
    rf'\1\n{new_services_html}\n        \3',
    content,
    flags=re.DOTALL
)

# Save the updated HTML
with open(html_file, "w", encoding="utf-8") as file:
    file.write(updated_content)

print("✅ Services updated successfully!")


import re
import os
import shutil

# html_file = "User_Portfolio/tester3.html"

with open(html_file, "r", encoding="utf-8") as file:
    content = file.read()

# === Update PROJECTS SECTION ===

projects_pattern = re.search(r'(<div class="projects-grid">)(.*?)(</div>\s*</section>)', content, re.DOTALL)

if not projects_pattern:
    print("Projects section not found in the file.")
else:
    print("Let's add new projects!")
    print("You'll be prompted for each field.")

    projects = []
    while True:
        name = input("\nProject Name (or press ENTER to stop): ").strip()
        if not name:
            break
        desc = input("Project Description: ").strip()
        # Clean the path by removing extra quotes and fixing backslashes
        original_img_path = input("Image Path (can be full path or URL): ").strip().replace("\\", "/")
        original_img_path = original_img_path.strip('"')  # Remove any surrounding quotes

        # Ensure destination folder exists
        destination_folder = "User_Portfolio"
        os.makedirs(destination_folder, exist_ok=True)

        # Extract filename and copy it as is, without URL encoding
        img_filename = os.path.basename(original_img_path)
        copied_img_path = os.path.join(destination_folder, img_filename)

        try:
            shutil.copy(original_img_path, copied_img_path)
        except Exception as e:
            print(f"Error copying the image: {e}")
            continue

        # Use relative path for HTML (without URL encoding)
        relative_img_path = img_filename  # Directly use the filename with spaces

        projects.append({
            "name": name,
            "desc": desc,
            "img": relative_img_path  # Store the image path as is
        })

    # Construct the new projects HTML to insert
    new_projects_html = ""
    for proj in projects:
        new_projects_html += f'''
            <div class="project-card">
                <img src="{proj["img"]}" alt="{proj["name"]}">
                <h3>{proj["name"]}</h3>
                <p>{proj["desc"]}</p>
                <div class="btn-group">
                    <div class="btn">Live Demo</div>
                    <div class="btn">Github</div>
                </div>
            </div>'''

    # Replace the old section with the new one
    updated_content = re.sub(
        r'(<div class="projects-grid">)(.*?)(</div>\s*</section>)',
        rf'\1{new_projects_html}\3',
        content,
        flags=re.DOTALL
    )

    # Write the updated content back to the HTML file
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(updated_content)

    print("\n✅ Projects section updated successfully.")
