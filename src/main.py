import os
import shutil
from copy_recursive import copy_files_recursive
from generate_page import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    abs_dest_dir = os.path.abspath(dir_path_public)
    # delete contents of destination directory, if it exists
    if os.path.exists(abs_dest_dir):
        print(f"Deleting pre-existing destination directory: {abs_dest_dir}")
        shutil.rmtree(abs_dest_dir)
    else:
        print("No pre-existing destination direcory")

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    generate_page("./content/index.md", template_path, "./public/index.html")

    generate_page(
        "./content/blog/glorfindel/index.md",
        template_path,
        "./public/blog/glorfindel/index.html",
    )
    generate_page(
        "./content/blog/tom/index.md", template_path, "./public/blog/tom/index.html"
    )
    generate_page(
        "./content/blog/majesty/index.md",
        template_path,
        "./public/blog/majesty/index.html",
    )
    generate_page(
        "./content/contact/index.md", template_path, "./public/contact/index.html"
    )


if __name__ == "__main__":
    main()
