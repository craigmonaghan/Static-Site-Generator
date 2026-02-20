import os, sys
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
        split_markdown = markdown.split("\n")
        for line in split_markdown:
            if line.startswith("# "):
                return line[2:].strip()
        raise Exception("Markdown must contain an H1 header")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
         markdown_content = file.read()

    with open(template_path) as file:
         html_template = file.read()

    htmlstring = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    html_template = html_template.replace("{{ Title }}", title)
    html_template = html_template.replace("{{ Content }}", htmlstring)
    html_template = html_template.replace('href="/', f'href="{basepath}')
    html_template = html_template.replace('src="/', f'src="{basepath}')

    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    with open(dest_path, "w") as file:
         file.write(html_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
     for i in os.listdir(dir_path_content):
          dir_path = os.path.join(dir_path_content, i)
          d_dir_path = os.path.join(dest_dir_path, i)
          if os.path.isfile(dir_path):
               md_to_html = i.replace(".md", ".html")
               d_dir_path = os.path.join(dest_dir_path, md_to_html)
               generate_page(dir_path, template_path, d_dir_path, basepath)
          elif os.path.isdir(dir_path):
               generate_pages_recursive(dir_path, template_path, d_dir_path, basepath)