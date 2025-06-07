import os
import shutil
import sys
from copy_recursive import copy_files_recursive
from generate_page import generate_pages_recursive

dir_path_static = "./static"

# dir_path_public = "./public"
dir_path_public = "./docs"  # GitHub pages default

dir_path_content = "./content"
template_path = "./template.html"


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    else:
        basepath = "/"

    abs_dest_dir = os.path.abspath(dir_path_public)
    # delete contents of destination directory, if it exists
    if os.path.exists(abs_dest_dir):
        print(f"Deleting pre-existing destination directory: {abs_dest_dir}")
        shutil.rmtree(abs_dest_dir)
    else:
        print("No pre-existing destination direcory")

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print(f"Recursively generating html pages from markdown in {dir_path_content}...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
