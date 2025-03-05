# Function to generate homepage based on user choice
def generate_homepage(template, user_info):
    from datetime import datetime

    # Generate project list
    project_template = """
        <li>
            <h3>{name}</h3>
            <p>{description}</p>
        </li>
    """
    project_list = ""
    for project in user_info["projects"]:
        project_list += project_template.format(name=project["name"], description=project["description"])

    # Get current year
    current_year = datetime.now().year

    # Combine all data with HTML template
    homepage = template.format(
        name=user_info["name"],
        about="This is a placeholder about me section.",
        work=user_info["occupation"],
        projects=project_list,
        email=user_info["contact"]["email"],
        phone=user_info["contact"]["Phone num"],
        github="https://github.com/12ripvanwinkle"
    )
    
    # Save the generated HTML to a file
    with open('index.html', 'w') as file:
        file.write(homepage)
    print("HTML file generated successfully!")

# Define templates
template_1 = """
<!DOCTYPE html>
<html>
<head>
    <title>{name} - Personal Website</title>
</head>
<body>
    <h1>Welcome to {name}'s Personal Website template 1</h1>
    <p>About me: {about} {work}</p>
    <ul>
        {projects}
    </ul>
    <p>Contact: {email} | {phone}</p>
</body>
</html>
"""

template_2 = """
<!DOCTYPE html>
<html>
<head>
    <title>{name}'s Professional Page</title>
</head>
<body>
    <h1>{name}'s Work template 2</h1>
    <p>Occupation: {work}</p>
    <h2>Projects</h2>
    <ul>
        {projects}
    </ul>
    <footer>
        Contact me at: {email}
    </footer>
</body>
</html>
"""

# Menu for user choice
while True:
    print("Choose an option:")
    print("1. Generate Template 1")
    print("2. Generate Template 2")
    print("3. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        # Collect user info
        user_info = {
            "name": input('Enter your name: '),
            "occupation": input('Enter your occupation: '),
            "projects": [
                {"name": "Project 1", "description": "This is my first project"},
                {"name": "Project 2", "description": "This is my second project"}
            ],
            "contact": {
                "email": input("Enter your email: "),
                "Phone num": input("Enter your phone number: ")
            }
        }
        generate_homepage(template_1, user_info)
    
    elif choice == "2":
        # Collect user info for template 2
        user_info = {
            "name": input('Enter your full name: '),
            "occupation": input('Enter your job title: '),
            "projects": [
                {"name": "Portfolio Project", "description": "Showcasing my portfolio"},
                {"name": "Team Project", "description": "Collaborated with a team"}
            ],
            "contact": {
                "email": input("Enter your work email: "),
                "Phone num": input("Enter your contact number: ")
            }
        }
        generate_homepage(template_2, user_info)
    
    elif choice == "3":
        print("Exiting the program. Goodbye!")
        break
    
    else:
        print("Invalid choice, please try again.")

