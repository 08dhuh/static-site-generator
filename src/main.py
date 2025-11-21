#from textnode import TextNode, TextType
import os, shutil, sys
from helper import generate_pages_recursive

def copy_files(source, dest):
    if not os.path.exists(source):
        raise ValueError("invalid source")  
    if os.path.exists(dest):
        shutil.rmtree(dest) 
    os.makedirs(dest)
    for f in os.listdir(source):
        if os.path.isfile(os.path.join(source, f)):
            shutil.copy(os.path.join(source, f), os.path.join(dest,f))
            continue
        copy_files(os.path.join(source, f),os.path.join(dest,f))

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    #copy_files("static", "public")
    if not basepath.endswith("/"):
        basepath += "/"

    generate_pages_recursive('content',
                  'template.html',
                  'docs',
                  "/")
    #tn = TextNode("what",TextType.BOLD)
    #print(tn)

if __name__=='__main__':
    main()