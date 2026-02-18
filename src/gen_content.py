import os, htmlnode
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
        split_markdown = markdown.split("\n")
        for line in split_markdown:
            if line.startswith("# "):
                return line[2:].strip()
        raise Exception("Markdown must contain an H1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
         markdown_content = file.read()

    with open(template_path) as file:
         html_template = file.read()

    htmlstring = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", htmlstring)

    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    with open(dest_path, "w") as file:
         file.write(html_template)
    
    print(f"{htmlstring}")