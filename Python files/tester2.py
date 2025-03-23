import random
import re

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

def animations_tester():
    # Read the CSS file
    css_file_path = "Portfolio_templates/portfolio_template_style1.css"
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
    animations_tester()
