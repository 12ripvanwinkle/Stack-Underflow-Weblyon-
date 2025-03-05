from bs4 import BeautifulSoup

# Read the HTML file
html_file = "Portfolio_templates/portfolio_template_0_copy.html"  # Update with your file path
with open(html_file, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find the skills list
skills_list = soup.find("div", class_="skills").find("ul")
skills = [li.text.strip() for li in skills_list.find_all("li")]

# Display current skills
print("Current Skills:")
for idx, skill in enumerate(skills, 1):
    print(f"{idx}. {skill}")

# Prompt user to remove skills
while True:
    to_remove = input(
        "Enter the number of the skill to remove (or 'done' to finish): ").strip()
    if to_remove.lower() == "done":
        break
    if to_remove.isdigit():
        skill_index = int(to_remove) - 1
        if 0 <= skill_index < len(skills):
            removed_skill = skills.pop(skill_index)
            print(f"Removed: {removed_skill}")
        else:
            print("Invalid number. Try again.")
    else:
        print("Invalid input. Please enter a number or 'done'.")

# Update the HTML
skills_list.clear()
for skill in skills:
    new_li = soup.new_tag("li")
    new_span = soup.new_tag("span")
    new_icon = soup.new_tag("i", attrs={"class": "bx bx-chevron-right"})
    new_span.append(new_icon)
    new_span.append(f" {skill}")
    new_li.append(new_span)
    skills_list.append(new_li)

# Save the updated HTML
output_file = "updated_portfolio.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(str(soup))

print(f"Updated HTML saved to {output_file}")
