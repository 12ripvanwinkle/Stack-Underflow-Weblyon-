# User details
user_info = {
    "name" : input('Enter your name: '),
    "occupation" : input('Enter your occupation: '),
    "projects" : [
        {"name": "project 1", "description": "this is my project"},
        {"name": "project 1", "description": "this is my project"},
    ],

    "contact": {
        "email" : input("Enter your email: "),
        "Phone num" : input("Enter your phone number: ")
    }
}

# Html template
homepage_template = """
<!DOCTYPE html>
<html>
<head>
    <title>{name} - Personal Website </title>
    <link rel = "stylesheet" href = "styles.css">
</head>
<body>
    <header>
        <h1>{name}</h1>
    </header>
    <nav>
        <ul>
            <li><a href="#about">About</li>
            <li><a href="#projects">Projects</li>
            <li><a href="#contact">Contact</li>
        </ul>
    </nav>
    <main>
        <section id="about">
            <h2>About Me</h2>
            <p>{about} {work}</p>
        </section>
        <section id="projects">
            <h2>Projects/<h2>
            <ul>
                {projects}
            </ul>
        </section>
        <section id="contact">
            <h2>Contact</h2>
            <ul>
                <li>Email: <a href="mailto: {email}">{email}</a><li>
                <li>Phone: {phone}</li>
                <li>Github: <a href="{github}" target="_blank">{github}</a></li>
            </ul>
        </section>
    </main>
    <footer>
        <p>ello govna</p>
    </footer>
</body>
</html>
"""

project_template1= """
    <li>
        <h3>{name}</h3>
        <p>{description}</p>
    </li>
"""

# generate project list
project_list = ""
for project in user_info ["projects"]:
    project_list += project_template1.format(name=project["name"], description= project["description"])
""
from datetime import datetime
current_year = datetime.now().year

# combine all data with html template
homepage = homepage_template.format(
    name = user_info["name"],
    about = "This is a placeholder about me section.",
    work = user_info["occupation"],
    projects = project_list,
    email = user_info["contact"]["email"],
    phone = user_info["contact"]["Phone num"],
    github = "https://github.com/12ripvanwinkle"
)


# save the generated html to a file
with open('index.html','w') as file:
    file.write(homepage)