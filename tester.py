import re
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Ollama Model Setup
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model  # Chain together using LangChain

def ask_ollama():
    """Ask Ollama for web development skills."""
    question = "What are common skills for Web Developers?"
    response = chain.invoke({"context": "", "question": question})
    return response

def extract_skills(ai_response):
    """Extracts all skill-like words/phrases from the AI response."""
    skills = set()  # Avoid duplicates
    lines = ai_response.split("\n")

    for line in lines:
        match = re.match(r"\d+\.\s*(.+)", line)
        if match:
            extracted_skills = match.group(1).split(", ")  # Split multiple skills in a line
            skills.update(extracted_skills)  # Add to set to avoid duplicates
        else:
            words = line.strip().split()
            if len(words) < 5:  # Avoid long sentences
                skills.update(words)

    return sorted(skills)  # Return sorted skills list

def update_html_skills(html_file_path, skills):
    """Replaces the existing skills list in the HTML file."""
    if not os.path.exists(html_file_path):
        print("Error: HTML file not found.")
        return

    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Generate new skills list in HTML format
    new_skills_html = "\n".join([
        f'                    <li><span><i class="bx bx-chevron-right"></i> {skill}</span></li>'
        for skill in skills
    ])

    # Replace the old skills list
    updated_html = re.sub(
        r'<div class="skills">\s*<ul>.*?</ul>\s*</div>',
        f'<div class="skills">\n                <ul>\n{new_skills_html}\n                </ul>\n            </div>',
        html_content,
        flags=re.DOTALL
    )

    # Save the updated HTML file
    with open(html_file_path, "w", encoding="utf-8") as file:
        file.write(updated_html)

    print("✅ Skills section updated successfully!")

if __name__ == "__main__":
    ollama_response = ask_ollama()
    print("🔄 Fetching skills from Ollama...")
    print("🔍 Extracting skills...")
    skills_list = extract_skills(ollama_response)
    
    if skills_list:
        print("📄 Updating HTML file...")
        update_html_skills("Portfolio_templates/portfolio_template_0 copy2.html", skills_list)
        print("🎉 Update complete!")
    else:
        print("⚠️ No skills extracted. Check the AI response.")
