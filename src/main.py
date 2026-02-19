import os, shutil
from gen_content import generate_pages_recursive
def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        print("cleared directory ")
    os.mkdir("./public")
    copy_files_recursive("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")

    
def copy_files_recursive(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            os.mkdir(dest_path)
            print("Directory created")
            copy_files_recursive(source_path, dest_path)
            print("Recursion is happening")
        else:
            print(f"Files created {dest_path}")
            shutil.copy(source_path, dest_path)


if __name__ == "__main__":
    main()