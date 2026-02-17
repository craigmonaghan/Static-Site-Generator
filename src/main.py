import os, shutil


def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
        print(f"cleared directory ")
    os.mkdir("./public")
    copy_files_recursive("./static", "./public")

    
def copy_files_recursive(source, destination):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(source_path):
            os.mkdir(dest_path)
            print(f"Directory created")
            copy_files_recursive(source_path, dest_path)
            print(f"Recursion is happening")
        else:
            print(f"Files created {dest_path}")
            shutil.copy(source_path, dest_path)


if __name__ == "__main__":
    main()