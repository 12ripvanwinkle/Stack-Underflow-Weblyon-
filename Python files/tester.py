import random
import re
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

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

# Animation styles
animation_styles = [
    ("fadeIn", "opacity: 0;", "opacity: 1;"),
    ("slideUp", "transform: translateY(100px); opacity: 0;", "transform: translateY(0); opacity: 1;"),
    ("zoomIn", "transform: scale(0.7); opacity: 0;", "transform: scale(1); opacity: 1;"),
    ("slideLeft", "transform: translateX(-50px); opacity: 0;", "transform: translateX(0); opacity: 1;")
]

template = """
Answer the question below.
Here is the conversation history: {context}
Question: {question}
Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def ai_helper(web_type):
    context = "just list the order and beside it put a very brief reason no need to add anything else"
    if web_type == "Portfolio":
        ai_input = f"what would be the order for the best layout for a portfolio website given that I have a header, home section, about me section, services section, contact section and footer section"
        result = chain.invoke({"context": context, "question": ai_input})
        print("Bot: ", result)
        context += f"\nUser: {ai_input}\nAI: {result}"
    else:
        ai_input = f"what would be the order for the best layout for a business website given that I have a header, home section, about/history section, products section, reviews section and footer section"
        result = chain.invoke({"context": context, "question": ai_input})
        print("Bot: ", result)
        context += f"\nUser: {ai_input}\nAI: {result}"

def layout_chooser(user_choice):
    layouts = [
        ["Header section", "Home section", "About me section", "Services section", "Contact section", "Footer section"],
        ["Header section", "Home section", "About/History section", "Products section", "Reviews section", "Footer section"]
    ]
    
    if user_choice == "Portfolio":
        print("From the Portfolio sections are: ")
        sections = layouts[0]
        for i, section in enumerate(sections):
            print(f"{i + 1}. {section}")
        print("Enter the order you wish by separated commas (e.g., 1,2,3,4,5,6): ")
        order = input("Your order: ")
        
        try:
            order = [int(num.strip()) - 1 for num in order.split(",")]
            if len(set(order)) != len(sections) or not all(0 <= num < len(sections) for num in order):
                raise ValueError("Invalid order")
            ordered_sections = [sections[i] for i in order]
            print("Ordered sections:", ordered_sections)
            return ordered_sections
        except (ValueError, IndexError):
            print("Invalid input. Please enter the numbers in the correct order.")
    else:
        print("From the Ecommerce sections below, choose your order by entering the number associated: ")
        sections = layouts[1]
        for i, section in enumerate(sections):
            print(f"{i + 1}. {section}")

def font_chooser():
    print("Available Fonts: ")
    font_names = list(font_dict.keys())
    for i, font in enumerate(font_names):
        print(f"{i}. {font}")
    try:
        choice = int(input("Choose your font by entering the corresponding number: "))
        if 0 <= choice < len(font_names):
            selected_font = font_names[choice]
            font_url = font_dict[selected_font]

            print(f"Selected font: {selected_font}")
            # Read the existing CSS file
            try:
                with open("Portfolio_templates/portfolio_template_style1.css", "r") as css_file:
                    original_css = css_file.read()

                # Replace "Poppins" with the selected font in the entire CSS
                updated_css = re.sub(r'"Poppins"', f'"{selected_font}"', original_css)
                updated_css = re.sub(r'Poppins', selected_font, updated_css)

                # Add the font import at the top of the CSS if not already present
                updated_css = f"@import url('{font_url}');\n" + updated_css

                # Now, call the color_chooser to apply color changes
                updated_css = color_chooser(updated_css)

                # Write the final updated CSS to a new file
                updated_css_path = "portfolio_template_style1_updated.css"
                with open(updated_css_path, "w") as updated_css_file:
                    updated_css_file.write(updated_css)

                print(f"Font and colors applied successfully to the new CSS file: {updated_css_path}")
                
                return selected_font

            except FileNotFoundError:
                print("Original CSS file not found. Please make sure the file path is correct.")
                return None
        else:
            print("Invalid choice. Please select a valid font number")
            return font_chooser()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

def color_chooser(css_content):
    print("Available color sets: ")
    # Display available color sets
    for i, color_set in enumerate(color_set_word):
        print(f"{i}. {color_set}")

    try:
        # Get user choice for color set
        choice = int(input("Choose your color set by entering the corresponding number: "))
        if 0 <= choice < len(color_sets):
            selected_colors = color_sets[choice]
            print("Selected color set: ", selected_colors)
            
            # Apply the selected colors to the CSS content
            new_css = css_content
            for var, color in selected_colors.items():
                new_css = new_css.replace(f"var({var})", color)

            return new_css
        
        else:
            print("Invalid input. Please enter a number.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


# Generate random animation CSS
def generate_animation_css():
    animation_css = ""
    for animation_name, start_state, end_state in animation_styles:
        duration = round(random.uniform(0.5, 2.5), 1)
        delay = round(random.uniform(0, 1), 2)
        animation_css += f"""
@keyframes {animation_name} {{
    0% {{ {start_state} }}
    100% {{ {end_state} }}
}}
"""
    return animation_css

# Animation chooser function
def animations_chooser():
    print("Available animation sets: ")
    for i, animation_style in enumerate(animation_styles):
        print(f"{i}. {animation_style[0]}")

    # Read the CSS file
    css_file_path = "portfolio_template_style1_updated.css"
    with open(css_file_path, "r", encoding="utf-8") as css_file:
        css_content = css_file.read()

    # Generate random animation CSS
    animation_css = generate_animation_css()
    
    # Initialize css_content_updated to an empty string and insert the generated animation CSS
    css_content_updated = css_content + "\n" + animation_css

    # Apply animations to elements
    elements = [".home-content h3", ".home-content h1", ".home-content p", ".social-icons a", ".btn", ".about-content p", ".services h2", ".service-box", ".service-info p", ".contact"]
    for element in elements:
        random_animation = random.choice(animation_styles)
        animation_name = random_animation[0]
        duration = round(random.uniform(0.5, 2.5), 1)
        delay = round(random.uniform(0, 1), 2)

        css_content_updated += f"""
{element} {{
    opacity: 0; /* Start invisible */
    transform: translateY(50px); /* Start off-screen */
    transition: opacity 1s ease-out, transform 1s ease-out; /* Set up the transition */
}}

{element}.visible {{
    animation: {animation_name} {duration}s ease-out {delay}s forwards;
}}
"""
    # Save the updated CSS file
    randomized_css_filename = "portfolio_template_style1_updated.css"
    with open(randomized_css_filename, "w", encoding="utf-8") as randomized_css_file:
        randomized_css_file.write(css_content_updated)

    # Add JavaScript for Intersection Observer
    html_content_updated = ''
    html_content_updated += """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('.home-content h3, .home-content h1, .home-content p, .social-icons a, .btn, .about-content p, .services h2, .service-box, .service-info p, .contact');

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Stop observing once the element is visible
            }
        });
    }, { threshold: 0.1 }); // Trigger when 10% of the element is in view

    elements.forEach(element => observer.observe(element));
});
</script>
"""

    # Save the updated HTML file
    with open("ordered_portfolio.html", "a", encoding="utf-8") as randomized_html_file:
        randomized_html_file.write(html_content_updated)

def html_generator(ordered_sections):
    if not ordered_sections:
        print("No ordered sections provided. Exiting.")
        return

    try:
        name = input("Enter the portfolio name: ")

        html_content = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="portfolio_template_style1_updated.css">
            <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
            <title>{name} Personal Portfolio</title>
        </head>
        <body>
        """
        with open("Portfolio_templates/portfolio_template_1.html", "r") as file:
            html_template = file.read()

        for section in ordered_sections:
            pattern = rf"<!-- {re.escape(section)} -->(.*?)<!-- END -->"
            match = re.search(pattern, html_template, re.DOTALL)
            
            if match:
                html_content += match.group(0) + "\n"
            else:
                print(f"Warning: Section '{section}' not found in the template.")

        html_content += """
        </body>
        </html>
        """

        with open("ordered_portfolio.html", "w") as new_file:
            new_file.write(html_content)

        print("Generated ordered_portfolio.html with your chosen layout!")
    except FileNotFoundError:
        print("Template file not found. Make sure the file path is correct.")

if __name__ == "__main__":
    result = layout_chooser("Portfolio")
    html_generator(result)
    font_chooser()
    animations_chooser()