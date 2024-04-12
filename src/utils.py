from markdown import markdown_to_html_node, extract_title
import os
import shutil


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_entries = os.listdir(dir_path_content)
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for dir_entry in dir_entries:
        from_path = os.path.join(dir_path_content, dir_entry)
        to_path = os.path.join(dest_dir_path, dir_entry)

        if os.path.isdir(os.path.join(dir_path_content, dir_entry)):
            generate_pages_recursive(from_path, template_path, to_path)
            continue

        generate_page(from_path, template_path, to_path.replace(".md", ".html"))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file:
        markdown = from_file.read()

    with open(template_path, "r") as template_file:
        template = template_file.read()

    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    with open(dest_path, "w") as dest:
        dest.write(template)


def copy_files(from_path, to_path):
    dir_entries = os.listdir(from_path)
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    os.mkdir(to_path)

    for dir_entry in dir_entries:
        dir_entry_path = os.path.join(from_path, dir_entry)
        if os.path.isdir(dir_entry_path):
            copy_files(os.path.join(from_path, dir_entry), os.path.join(to_path, dir_entry))
            continue

        shutil.copy(dir_entry_path, to_path)
