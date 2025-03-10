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
    "Playfair Display": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&display=swap"
}

# Predefined color sets (same as before)
color_sets = [
    {
        "--bg-color": "#080808",
        "--second-bg-color": "#001005",
        "--text-color": "white",
        "--main-color": "#00ff51"
    },
    {
        "--bg-color": "#080808",
        "--second-bg-color": "#101010",
        "--text-color": "white",
        "--main-color": "#ea580c"
    },
    {
        "--bg-color": "#080808",
        "--second-bg-color": "#1b0000",
        "--text-color": "white",
        "--main-color": "#f60b0b"
    },
    {
        "--bg-color": "#080808",
        "--second-bg-color": "#101010",
        "--text-color": "white",
        "--main-color": "#ca0bf5"
    },
    {
        "--bg-color": "#f9f9f9",
        "--second-bg-color": "#d2ffd1",
        "--text-color": "black",
        "--main-color": "#2E8B57"
    },
    {
        "--bg-color": "#080808",
        "--second-bg-color": "#101010",
        "--text-color": "white",
        "--main-color": "#ea119b"
    }
]

# Function to generate a random font from the font dictionary
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
        with open(css_file_path, "r") as css_file:
            css_content = css_file.read()

        # Add Google Fonts import at the top and update :root with the selected colors and font
        css_content_updated = f"{google_font_import}\n" + re.sub(
            r":root\s*{[^}]+}",
            f""":root {{
            --bg-color: {selected_colors["--bg-color"]};
            --second-bg-color: {selected_colors["--second-bg-color"]};
            --text-color: {selected_colors["--text-color"]};
            --main-color: {selected_colors["--main-color"]};
            --font-family: '{selected_font}', sans-serif; /* Use the random font-family */
        }}""",
            css_content
        )

        # Now apply the selected font-family globally to all elements by updating the * selector
        css_content_updated = re.sub(
            r'font-family:\s*"Poppins",\s*sans-serif;',
            f'font-family: "{selected_font}", sans-serif;',  # Replace Poppins with the random font
            css_content_updated
        )

        # Randomly adjust margins and paddings
        css_content_updated = re.sub(
            r'(margin|padding):\s*\d+px;',
            lambda match: f"{match.group(1)}: {random.randint(5, 50)}px;",
            css_content_updated
        )

        # Save the updated CSS file
        randomized_css_filename = "randomized_portfolio_style.css"
        with open(randomized_css_filename, "w") as randomized_css_file:
            randomized_css_file.write(css_content_updated)

        # Read the HTML file
        html_file_path = "Portfolio_templates/portfolio_template_1.html"
        with open(html_file_path, "r") as html_file:
            html_content = html_file.read()

        # Update the CSS link and add the Google Fonts link in the HTML file
        html_content_updated = re.sub(
            r'<link\s+rel="stylesheet"\s+href="[^"]+">',
            f'<link rel="stylesheet" href="{randomized_css_filename}">',
            html_content
        )

        # Shuffle sections in the HTML file
        sections = re.findall(r'(<section.*?>.*?</section>)', html_content_updated, re.DOTALL)
        random.shuffle(sections)

        # Replace original sections with shuffled ones
        html_content_updated = re.sub(
            r'(<section.*?>.*?</section>)',
            lambda _: sections.pop(0),
            html_content_updated,
            count=len(sections)
        )

        # Save the updated HTML file
        with open("randomized_portfolio.html", "w") as randomized_html_file:
            randomized_html_file.write(html_content_updated)
    else:
        pass


if __name__ == "__main__":
    Randomiser("Portfolio_templates")
