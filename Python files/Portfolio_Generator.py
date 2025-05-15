# code for portfolio generators exclusively
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import os
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

def user_info_getter(portfolio_type):
    name = input("Enter your name: ")
    occupation = input("Enter your occupation: ")
    pfp = input("Enter the path to your profile picture: ").strip('"')
    if portfolio_type == 0:
        ai_ans = input("Do you want to use AI to generate your portfolio? (y/n): ").lower()
        
        if ai_ans == "y":

            print("The ai is generating text for you")
            intro1 = ai_helper(occupation, 1, "Portfolio")
            print("The ai is generating somemore text for you")
            about_me_info = ai_helper(occupation, 2, "Portfolio")
        else:
            intro1 = input("Enter a 15 word short intro about you for the hero section: \n")
            about_me_info = input("Enter a 40 word extract about you for the about me section: \n")
        user_info = {
            "name": name,
            "occupation": occupation,
            "pfp":pfp,
            "intro1": intro1,
            "about_me_info": about_me_info
        }
    else:

        user_info = {
            "name": name,
            "occupation": occupation,
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

        
def portfolio0_skill_getter():
    skills = {}
    print("Enter information for 3 services:\n")

    for i in range(1, 4):
        skill = input(f"Enter title for Skill {i}: ").strip()
        description = input(f"Enter description for Skill {i}: ").strip()

        skills[f"skill{i}"] = skill if skill.lower() != "no" else ""
        skills[f"skill_text{i}"] = description if description.lower() != "no" else ""

    return skills

def portfolio_type():
    print("Enter the portfolio of your choosing by entering the corresponding number")
    # Make it proper names and not just 0,1,2
    choice = input("0. Portfolio 0\n1. Portfolio 1\n2. Portfolio 2\n")
    match choice:
        case "0":
            print("Portfolio 0")
            user_info = user_info_getter(0)
            contact_info = contact_info_getter()
            skills_info = portfolio0_skill_getter()

            # Merge dictionaries
            info = {**user_info, **contact_info, **skills_info}
            print(info)  # Debug print
            template = load_template("Portfolio_templates/portfolio_template_0.html")

            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_style0.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio"

            # Copy the file
            shutil.copy(source_path, destination_folder)

            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_script0.js"
            shutil.copy(source_path, destination_folder)

            generator(info, template, False,0)

        case "1":
            print("Portfolio 1")
            user_info = user_info_getter(0)
            print(user_info)  # Debug print
            template = load_template("Portfolio_templates/portfolio_template_1.html")

            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_style1.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio"
            # Copy the file
            shutil.copy(source_path, destination_folder)



            generator(user_info, template, True,0)
        case "2":
            print("Portfolio 2")
            user_info = user_info_getter(1)
            print(user_info)  # Debug print
            template = load_template("Portfolio_templates/portfolio_template_2.html")

            # Define the source and destination paths
            source_path = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\Portfolio_templates\portfolio_template_style2.css"
            destination_folder = r"C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio"

            # Copy the file
            shutil.copy(source_path, destination_folder)


            generator(user_info, template, True, 1)

        case _:
            print("Invalid choice")
            portfolio_type()

def update_skills(html_file, services, special):
    # Read the existing HTML file
    with open(html_file, "r", encoding="utf-8") as file:
            content = file.read()
    if services == False:
        # Extract the current skills list using regex
        skills_pattern = re.search(r'(<div class="skills">\s*<ul>)(.*?)(</ul>\s*</div>)', content, re.DOTALL)

        if not skills_pattern:
            print("Skills section not found in the file.")
            return

        # Capture editable comments before replacing
        editable_comments = re.findall(r'<!--editable: skill\d+-->', skills_pattern.group(2))

        # Prompt the user for new skills
        new_skills = input("Enter skills separated by commas: ").split(",")

        # Trim whitespace and remove empty entries
        new_skills = [skill.strip() for skill in new_skills if skill.strip()]

        # Generate new <li> elements for the skills
        # Re-attach the editable comments if available
        new_skills_html_lines = []
        for i, skill in enumerate(new_skills):
            comment = f'<!--editable: skill{i+1}-->' if i < len(editable_comments) else ''
            if comment:
                new_skills_html_lines.append(comment)
            new_skills_html_lines.append(f'<li><span><i class="bx bx-chevron-right"></i> {skill}</span></li>')

        new_skills_html = "\n".join(new_skills_html_lines)

        # Replace the existing skills with the new list
        updated_content = re.sub(
            r'(<div class="skills">\s*<ul>)(.*?)(</ul>\s*</div>)',
            rf'\1\n{new_skills_html}\n                \3',
            content,
            flags=re.DOTALL
        )
    else:
        if special == 1:
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
                    print("Invalid format. Use: Title, Years, Description")
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

            # # Replace old HTML block with new one
            # updated_content = re.sub(
            #     r'(<div class="services-container">\s*<div class="grid">)(.*?)(</div>\s*</div>)',
            #     rf'\1\n{new_services_html}\n        \3',
            #     content,
            #     flags=re.DOTALL
            # )

            # Projects section for portfolio website 2
            projects_pattern = re.search(r'(<div class="projects-grid">)(.*?)(</div>\s*</section>)', content, re.DOTALL)

            if not projects_pattern:
                print("Projects section not found in the file.")
            else:
                print("Time to add your projects")
                print("You will be prompted for the project name, description, and a picture")

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
                    
                # Start by applying the services update to original content
                updated_content = re.sub(
                    r'(<div class="services-container">\s*<div class="grid">)(.*?)(</div>\s*</div>)',
                    rf'\1\n{new_services_html}\n        \3',
                    content,
                    flags=re.DOTALL
                )

                # Then, if projects were added, update the projects section too
                if projects:
                    updated_content = re.sub(
                        r'(<div class="projects-grid">)(.*?)(</div>\s*</section>)',
                        rf'\1{new_projects_html}\3',
                        updated_content,  # 👈 apply to already updated services content
                        flags=re.DOTALL
                    )
            
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

def generator(info, template, wtype, special):
    # Move the image to the project folder
    destination_folder = "User_Portfolio"
    os.makedirs(destination_folder, exist_ok=True)

    # Copy the image to the destination folder
    destination_path = os.path.join(destination_folder, os.path.basename(info["pfp"]))
    shutil.copy(info["pfp"], destination_path)
      
    # Set the relative path for the HTML
    pfp_path = f"{os.path.basename(info['pfp'])}"

    # Use .get() to avoid KeyError if key doesn't exist
    if not info.get("phone") and not info.get("email") and info.get("address") and not info.get("intro1") and not info.get("about_me_info"):
        page = template.format(
            name = info["name"],
            occupation = info["occupation"],
            pfp = pfp_path,
            phone=info.get("phone", ""),  # Default to empty string if 'phone' doesn't exist
            email=info.get("email", ""),
            address=info.get("address", ""),
            intro1 = info.get("intro1", ""),  # Default to empty string if 'intro1' doesn't exist
            about_me_info = info.get("about_me_info", ""),
        )
    elif not info.get("phone") and not info.get("email") and not info.get("address"):
        page = template.format(
            name = info["name"], 
            occupation = info["occupation"],
            intro1 = info.get("intro1", ""),  # Default to empty string if 'intro1' doesn't exist
            about_me_info = info.get("about_me_info", ""),
            pfp = pfp_path,            
            phone=info.get("phone", ""),  # Default to empty string if 'phone' doesn't exist
            email=info.get("email", ""),
            address=info.get("address", "")
        )
    else:
        page = template.format(
                **info
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

    update_skills("User_Portfolio" + "\\" + file_name + ".html", wtype, special)

    # upload_project_file("C:\Users\nites\OneDrive\Desktop\Stack-Underflow-Weblyon-\User_Portfolio", 1, "js")

    # Open the HTML file in the default browser
    webbrowser.open(f"file://{os.path.abspath(file_path)}")

def load_template(file_path):
    """Read the HTML template from a file with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    # upload_project_file("C:\\Users\\nites\\OneDrive\\Desktop\\Stack-Underflow-Weblyon-\\User_Portfolio\\jsonTester.js", 1, "js")
    portfolio_type()
