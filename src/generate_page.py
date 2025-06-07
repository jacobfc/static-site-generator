from markdown_to_html import markdown_to_html_node, extract_title
import os


def get_file_contents(path):
    with open(path) as f:
        return f.read()


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from {from_path} to {dest_path},"
        "using template {template_path} and basepath {basepath}"
    )

    # get markdown file data, and template file data
    markdown = get_file_contents(from_path)
    template = get_file_contents(template_path)

    # convert markdown data to html, and extract page title
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    # populate template with converted markdown data
    output_html_page = (
        template.replace("{{ Title }}", title)
        .replace("{{ Content }}", html_content)
        .replace('href="/', f'href="{basepath}')
        .replace('src="/', f'src="{basepath}')
    )

    # create necessary folders for output file, if they don't already exist
    output_directory = os.path.dirname(dest_path)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # write html to output file
    output_file = open(dest_path, "w", encoding="utf-8")
    output_file.write(output_html_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        file_path = os.path.join(dir_path_content, filename)
        if os.path.isfile(file_path):  # call generate_page() on markdown files
            print(f"{file_path} is a file!")
            if filename.endswith(".md"):
                print(f"{file_path} ends with .md!")
                generate_page(
                    file_path,
                    template_path,
                    os.path.join(dest_dir_path, filename.rstrip(".md") + ".html"),
                    basepath,
                )
        else:  # recursively call function on directories
            print(f"{filename} is NOT a file, it's a directory!")
            generate_pages_recursive(
                file_path,
                template_path,
                os.path.join(dest_dir_path, filename),
                basepath,
            )
