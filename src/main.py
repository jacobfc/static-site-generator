import os
import shutil
from copy_recursive import copy_files_recursive

dir_path_static = "./static"
dir_path_public = "./public"


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


if __name__ == "__main__":
    main()
