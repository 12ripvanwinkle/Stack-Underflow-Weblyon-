import re
import random
import pinterestImageGetter 

# Predefined color sets
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

# Select a random color set
selected_colors = random.choice(color_sets)

# Read the CSS file
css_file_path = "Portfolio_templates/portfolio_template_style1.css"
with open(css_file_path, "r") as css_file:
    css_content = css_file.read()

# Replace the :root color variables with the selected color set
css_content_updated = re.sub(
    r":root\s*{[^}]+}",
    f""":root {{
    --bg-color: {selected_colors["--bg-color"]};
    --second-bg-color: {selected_colors["--second-bg-color"]};
    --text-color: {selected_colors["--text-color"]};
    --main-color: {selected_colors["--main-color"]};
}}""",
    css_content
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

# Update the CSS link in the HTML file
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

print("Randomization complete! Check 'randomized_portfolio.html' and 'randomized_portfolio_style.css'.")
