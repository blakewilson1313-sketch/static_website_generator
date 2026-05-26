from textnode import *
from htmlnode import *
from pathlib import Path
from inline_markdown import *
from markdown_blocks import *
import os
import sys
import shutil

def copy_static_to_public(source, dest):
    objects= os.listdir(source)
    for object in objects:
        current_path = os.path.join(source,object)
        new_dest = os.path.join(dest,object)
        if os.path.isfile(current_path):
            shutil.copy(current_path,dest)
        else: 
            if not os.path.exists(new_dest):
                os.mkdir(new_dest)
            copy_static_to_public(current_path, new_dest)
        
def main():
    src_path = "./static"
    new_dir_path = "./docs"    
    if os.path.exists(new_dir_path):
        shutil.rmtree(new_dir_path)
    os.mkdir(new_dir_path)
    copy_static_to_public(src_path, new_dir_path)
    basepath = sys.argv[0] if sys.argv[0] is not None else "/"
    generate_pages_recursive("./content","./template.html",new_dir_path, basepath)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
        

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as s:
        src_markdown = s.read()
    with open(template_path,"r") as t:
        template = t.read()
    html_rough = markdown_to_html_node(src_markdown)
    content = html_rough.to_html()
    title = extract_title(src_markdown)
    new_page = template.replace("{{ Title }}",title)
    new_page = new_page.replace("{{ Content }}",content)
    new_page = new_page.replace('href="/',f'href="{basepath}')
    new_page = new_page.replace('src="/',f'src="{basepath}')
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path,"w") as d:
        d.write(new_page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
    


        


main()