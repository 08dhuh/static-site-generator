#from textnode import TextNode, TextType
import os, shutil
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
    copy_files("static", "public")
    generate_pages_recursive('content',
                  'template.html',
                  'public')
    #tn = TextNode("what",TextType.BOLD)
    #print(tn)

if __name__=='__main__':
    main()