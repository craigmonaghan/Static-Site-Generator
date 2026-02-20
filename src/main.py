import os, shutil, sys
from gen_content import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
        print("cleared directory ")
    os.mkdir("./docs")
    copy_files_recursive("./static", "./docs")
    generate_pages_recursive("content", "template.html", "./docs", basepath)

    
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