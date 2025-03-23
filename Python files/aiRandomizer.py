# Randomiser tester stuff

import random
import re

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

# Animation styles
animation_styles = [
    ("fadeIn", "opacity: 0;", "opacity: 1;"),
    ("slideUp", "transform: translateY(100px); opacity: 0;", "transform: translateY(0); opacity: 1;"),
    ("rotateIn", "transform: rotate(360deg); opacity: 0;", "transform: rotate(0); opacity: 1;"),
    ("bounceIn", "transform: scale(0.5); opacity: 0;", "transform: scale(1); opacity: 1;"),
    ("zoomIn", "transform: scale(0.7); opacity: 0;", "transform: scale(1); opacity: 1;"),
    ("slideLeft", "transform: translateX(-50px); opacity: 0;", "transform: translateX(0); opacity: 1;")
]

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

# Generate a random font from the font dictionary
def generate_random_font():
    return random.choice(list(font_dict.keys()))

def Randomiser(filepath):
    selected_colors = random.choice(color_sets)
    selected_font = generate_random_font()

    # Dynamically generate the @import URL based on the selected font
    google_font_import = f"@import url('{font_dict[selected_font]}');"

    # Read the CSS file
    if filepath == "Portfolio_templates":
        css_file_path = "Portfolio_templates/portfolio_template_style1.css"
        with open(css_file_path, "r", encoding="utf-8") as css_file:
            css_content = css_file.read()

        # Generate random animation CSS
        animation_css = generate_animation_css()

        # Add Google Fonts import and update :root with selected colors and font
        css_content_updated = f"{google_font_import}\n" + re.sub(
            r":root\s*{[^}]+}",
            f""":root {{
            --bg-color: {selected_colors["--bg-color"]};
            --second-bg-color: {selected_colors["--second-bg-color"]};
            --text-color: {selected_colors["--text-color"]};
            --main-color: {selected_colors["--main-color"]};
            --font-family: '{selected_font}', sans-serif;
        }}""",
            css_content
        ) + animation_css

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
        randomized_css_filename = "randomized_portfolio_style.css"
        with open(randomized_css_filename, "w", encoding="utf-8") as randomized_css_file:
            randomized_css_file.write(css_content_updated)

        # Read the HTML file
        html_file_path = "Portfolio_templates/portfolio_template_1.html"
        with open(html_file_path, "r", encoding="utf-8") as html_file:
            html_content = html_file.read()

        # Update the CSS link and add the Google Fonts link in the HTML file
        html_content_updated = re.sub(
            r'<link\s+rel="stylesheet"\s+href="[^"]+">',
            f'<link rel="stylesheet" href="{randomized_css_filename}">',
            html_content
        )

        # Add JavaScript for Intersection Observer
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
        with open("randomized_portfolio.html", "w", encoding="utf-8") as randomized_html_file:
            randomized_html_file.write(html_content_updated)

if __name__ == "__main__":
    Randomiser("Portfolio_templates")
