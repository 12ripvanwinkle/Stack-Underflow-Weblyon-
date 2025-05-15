import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import random
from bs4 import BeautifulSoup
import os
import shutil
import webbrowser

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
# chains them together using langchain
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to the AI chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAI: {result}"
    
# Predefined font dictionary with the Google Fonts URL for each font
font_dict = {
    "Roboto": "https://fonts.googleapis.com/css2?family=Roboto:wght@100;300;400;500;700;900&display=swap",
    "Open Sans": "https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap",
    "Lato": "https://fonts.googleapis.com/css2?family=Lato:wght@100;300;400;500;700&display=swap",
    "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@100;300;400;500;700&display=swap",
    "Oswald": "https://fonts.googleapis.com/css2?family=Oswald:wght@200;300;400;500;600;700&display=swap",
    "Raleway": "https://fonts.googleapis.com/css2?family=Raleway:wght@100;200;300;400;500;600;700&display=swap",
    "Playfair Display": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap",
    "Tektur" : "https://fonts.googleapis.com/css2?family=Tektur:wght@400..900&display=swap"
}
# get fonts
def get_font_recommendations():
    print("\nHere are some font recommendations for your portfolio website:\n")

    for i, font in enumerate(font_dict.keys(), 1):
        question = f"Give a 7-word recommendation for using the font '{font}' for a portfolio website."
        result = chain.invoke({"context": "", "question": question})
        print(f"{i}. {font}\n   → {result}\n")

    try:
        choice = int(input("Enter the number of the font you want to choose: "))
        if 1 <= choice <= len(font_dict):
            selected_font = list(font_dict.keys())[choice - 1]
            font_url = font_dict[selected_font]
            print(f"\nYou selected: {selected_font}")
            return selected_font, font_url  # 👈 return both
        else:
            print("Invalid choice, please select a valid number.")
            return get_font_recommendations()
    except ValueError:
        print("Please enter a valid number.")
        return get_font_recommendations()


# Apply the selected font to the CSS file
def apply_font_to_css(selected_font, font_url, css_path="portfolio_template_style1.css"):
    try:
        with open(css_path, "r") as file:
            css_content = file.read()

        # Add the font import and update font-family
        css_content = f'@import url("{font_url}");\n\n' + css_content
        css_content = css_content.replace("font-family:", f"font-family: '{selected_font}', ")

        # Save the updated CSS
        updated_path = css_path.replace(".css", "_updated.css")
        with open(updated_path, "w") as file:
            file.write(css_content)

        print(f"✅ Font applied. Updated CSS saved to: {updated_path}")
        return updated_path

    except FileNotFoundError:
        print("❌ CSS file not found.")
        return None


# Predefined color sets
color_sets = [
    {"--bg-color": "#080808", "--second-bg-color": "#001005", "--text-color": "white", "--main-color": "#00ff51"},
    {"--bg-color": "#080808", "--second-bg-color": "#101010", "--text-color": "white", "--main-color": "#ea580c"},
    {"--bg-color": "#080808", "--second-bg-color": "#1b0000", "--text-color": "white", "--main-color": "#f60b0b"},
    {"--bg-color": "#080808", "--second-bg-color": "#101010", "--text-color": "white", "--main-color": "#ca0bf5"},
    {"--bg-color": "#f9f9f9", "--second-bg-color": "#d2ffd1", "--text-color": "black", "--main-color": "#2E8B57"},
    {"--bg-color": "#080808", "--second-bg-color": "#101010", "--text-color": "white", "--main-color": "#ea119b"}
]
color_set_word =[
    {"Back-ground color: ": "Very dark gray", "Second background color: ": "Very dark green", "Text color: " : "White", "Main color: ": "Bright green"},
    {"Back-ground color: ": "Very dark gray", "Second background color: ": "Dark gray", "Text color: " : "White", "Main color: ": "Bright Orange"},
    {"Back-ground color: ": "Very dark gray", "Second background color: ": "Very dark red", "Text color: " : "White", "Main color: ": "Bright Red"},
    {"Back-ground color: ": "Very dark gray", "Second background color: ": "Dark gray", "Text color: " : "White", "Main color: ": "Bright Purple"},
    {"Back-ground color: ": "Very light gray", "Second background color: ": "Very light green", "Text color: " : "Black", "Main color: ": "Medium Sea green"},
    {"Back-ground color: ": "Very dark gray", "Second background color: ": "Dark gray", "Text color: " : "White", "Main color: ": "Bright Pink"}
]

def choose_color_set(color_sets, color_set_word, model):
    print("\nChoose a color theme for your website:\n")

    for i, color_words in enumerate(color_set_word):
        readable_description = ", ".join(f"{k}{v}" for k, v in color_words.items())
        question = f"Give a 7-word recommendation for a color scheme like: {readable_description}"
        response = model.invoke(question)
        print(f"{i + 1}. {readable_description}\n   → {response}\n")

    while True:
        try:
            choice = int(input("Enter the number of your preferred color set: "))
            if 1 <= choice <= len(color_sets):
                selected_color_set = color_sets[choice - 1]
                print(f"\nYou selected: {color_set_word[choice - 1]}")
                print(f"Stored color values: {selected_color_set}")
                return selected_color_set
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

def apply_selected_color_to_css(css_path, selected_color_set):
    try:
        with open(css_path, "r") as file:
            css_content = file.read()

        # Replace all CSS variable placeholders with actual color values
        for var, color in selected_color_set.items():
            css_content = css_content.replace(f"var({var})", color)

        # Overwrite the same file (or create a new one if needed)
        with open(css_path, "w") as file:
            file.write(css_content)

        print(f"✅ Color set applied. CSS updated at: {css_path}")
        return css_path

    except FileNotFoundError:
        print("❌ CSS file not found.")
        return None

# Animation styles
animation_styles = [
    ("fadeIn", "opacity: 0;", "opacity: 1;"),
    ("slideUp", "transform: translateY(100px); opacity: 0;", "transform: translateY(0); opacity: 1;"),
    ("zoomIn", "transform: scale(0.7); opacity: 0;", "transform: scale(1); opacity: 1;"),
    ("slideLeft", "transform: translateX(-50px); opacity: 0;", "transform: translateX(0); opacity: 1;")
]

def choose_animation_style(animation_styles, model):
    print("\nChoose an animation style for your website:\n")

    for i, (name, from_style, to_style) in enumerate(animation_styles):
        description = f"Animation: {name}, From: {from_style}, To: {to_style}"
        question = f"Give a 7-word recommendation for animation like: {description}"
        response = model.invoke(question)
        print(f"{i + 1}. {name} → {response}")

    while True:
        try:
            choice = int(input("\nEnter the number of your preferred animation style: "))
            if 1 <= choice <= len(animation_styles):
                selected_animation = animation_styles[choice - 1]
                print(f"\nYou selected: {selected_animation[0]}")
                return selected_animation
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a number.")

def generate_animation_css(animation_style):
    name, from_style, to_style = animation_style
    return f"""
@keyframes {name} {{
    from {{
        {from_style}
    }}
    to {{
        {to_style}
    }}
}}
"""


def animations_chooser(html_content, css_path, animation_style):
    """
    Applies the selected animation style to predefined elements.

    Parameters:
    - html_content (str): HTML code as a string.
    - css_path (str): Path to the CSS file to be updated.
    - animation_style (tuple): Selected animation style tuple (name, ...).

    Returns:
    - updated_css_content (str): New CSS with animation rules.
    - updated_html_content (str): HTML with appended JS for animation trigger.
    """
    # Read the current CSS content
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Assume generate_animation_css() adds required @keyframes etc.
    animation_css = generate_animation_css(animation_style)  # You must already have this implemented
    css_content_updated = css_content + "\n" + animation_css

    elements = [
        ".home-content h3",
        ".home-content h1",
        ".home-content p",
        ".social-icons a",
        ".btn",
        ".about-content p",
        ".services h2",
        ".service-box",
        ".service-info p",
        ".contact"
    ]

    animation_name = animation_style[0]  # ✅ Use the selected animation

    for element in elements:
        duration = round(random.uniform(0.5, 2.5), 1)
        delay = round(random.uniform(0, 1), 2)

        css_content_updated += f"""
{element} {{
    opacity: 0;
    transform: translateY(50px);
    transition: opacity 1s ease-out, transform 1s ease-out;
}}

{element}.visible {{
    animation: {animation_name} {duration}s ease-out {delay}s forwards;
}}
"""

    # Add the JS for triggering .visible when elements scroll into view
    intersection_observer_js = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('.home-content h3, .home-content h1, .home-content p, .social-icons a, .btn, .about-content p, .services h2, .service-box, .service-info p, .contact');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    elements.forEach(el => observer.observe(el));
});
</script>
"""

    # Inject JS before </body> or at the end
    if "</body>" in html_content:
        html_content_updated = html_content.replace("</body>", intersection_observer_js + "\n</body>")
    else:
        html_content_updated = html_content + "\n" + intersection_observer_js

    return css_content_updated, html_content_updated

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
    pfp = input("Enter the path to your profile picture: ").strip('"')
    choice = input("Do you want to use AI to generate your portfolio? (y/n): ").lower()
    if choice == "y":
        print("The ai is generating text for you")
        intro1 = ai_helper(occupation, 1, "Portfolio")
        print("The ai is generating somemore text for you")
        about_me_info = ai_helper(occupation, 2, "Portfolio")
    else:
        intro1 = input("Enter a 15 word short intro about you for the hero section: \n")
        about_me_info = input("Enter a 40 word extract about you for the about me section: \n")
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    address = input("Entere your Parish/State/Province: ")
    user_info = {
            "name": name,
            "occupation": occupation,
            "pfp":pfp,
            "intro1": intro1,
            "about_me_info": about_me_info,
            "email": email,
            "phone": phone,
            "address": address
        }
    return user_info

def update_services_in_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        content = file.read()

    services_pattern = re.search(r'(<div class="services-container">)(.*?)(</div>\s*</section>)', content, re.DOTALL)
    if not services_pattern:
        print("Services section not found in the file.")
        return

    services_input = input("Enter services separated by commas (name: description): ").split(",")
    services = []

    for service in services_input:
        service = service.strip()
        if ':' in service:
            name, desc = service.split(':', 1)
            services.append((name.strip(), desc.strip()))
        else:
            print(f"Skipping invalid service entry (missing ':'): {service}")

    new_services_html = "\n".join([
        f'''
        <div class="service-box">
            <div class="service-info">
                <h4>{name}</h4>
                <p>{desc}</p>
            </div>
        </div>''' for name, desc in services])

    updated_content = re.sub(
        r'(<div class="services-container">)(.*?)(</div>\s*</section>)',
        rf'\1\n{new_services_html}\n        \3',
        content,
        flags=re.DOTALL
    )

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(updated_content)
    print("Services section updated successfully.")

def generate_portfolio_html(user_info, template_path, output_path, destination_folder="generated_images_portfolio"):
    # Make sure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Copy the profile picture to the destination folder
    if user_info.get("pfp") and os.path.isfile(user_info["pfp"]):
        destination_path = os.path.join(destination_folder, os.path.basename(user_info["pfp"]))
        shutil.copy(user_info["pfp"], destination_path)
        
        # Update the path in user_info to the relative path for HTML src
        user_info["pfp"] = destination_path
    else:
        print("⚠️ Profile picture not found or invalid path; skipping copy.")
        user_info["pfp"] = ""  # Or set a placeholder image path

    # Read the HTML template
    with open(template_path, 'r', encoding='utf-8') as file:
        template = file.read()

    # Replace placeholders with actual user data
    for key, value in user_info.items():
        template = template.replace(f"{{{key}}}", value)

    # Write the final HTML output
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(template)

    # Now update the services section inside the newly generated file
    update_services_in_html(output_path)

    print("✅ Portfolio HTML has been generated successfully.")

    # Open the generated portfolio in the default web browser
    abs_path = os.path.abspath(output_path)
    webbrowser.open(f"file://{abs_path}")



if __name__ == "__main__":
    updated_css_path = None
    final_css_path = None

    # Step 1: Select font
    result = get_font_recommendations()
    if result:
        selected_font, selected_font_url = result
        print(f"\n✅ Font selected: {selected_font}")
        print(f"🔗 Font URL: {selected_font_url}")
        updated_css_path = apply_font_to_css(selected_font, selected_font_url)
    else:
        print("⚠️ Font selection was skipped or failed.")

    # Step 2: Select color set
    if updated_css_path:
        selected_color_set = choose_color_set(color_sets, color_set_word, model)
        if selected_color_set:
            final_css_path = apply_selected_color_to_css(updated_css_path, selected_color_set)
        else:
            print("⚠️ Color selection was skipped or failed.")
    else:
        print("⚠️ Cannot apply colors because the font CSS path was not generated.")

    # Step 3: Select animation style and apply it
    if final_css_path:
        animation = choose_animation_style(animation_styles, model)
        if animation:
            print(f"\n🎬 Animation style selected: {animation}")

            # Read the current HTML
            html_path = "portfolio_template_1.html"
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # Apply animations to CSS and HTML
            new_css, new_html = animations_chooser(html_content, final_css_path, animation)

            # Save updated CSS
            with open(final_css_path, "w", encoding="utf-8") as f:
                f.write(new_css)

            # Save updated HTML
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(new_html)

            print("✅ Animations applied to HTML and CSS.")
        else:
            print("⚠️ Animation selection was skipped or failed.")

    
    # Step 5: Accept user details and apply it to the website
    user_info = user_info_getter()

    generate_portfolio_html(
        user_info,
        template_path="portfolio_template_1.html",  # path to your HTML with placeholders
        output_path="generated_portfolio.html"  # output file
    )
